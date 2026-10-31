import io
import json
from pathlib import Path
import struct
import tarfile
import tempfile
import unittest
from capsule import build_adapter_capsule, verify_adapter_capsule, sha, encoded, validate_adapter

BASE = {'model_id': 'toy', 'revision': 'frozen', 'weights_sha256': 'a' * 64}

def tensor(value=1.0):
    header = encoded({'weight': {'dtype': 'F32', 'shape': [1], 'data_offsets': [0, 4]}})
    return struct.pack('<Q', len(header)) + header + struct.pack('<f', value)

def branch(root):
    root.mkdir()
    data = tensor()
    adapter = {'base_pin': BASE, 'sha256': sha(data),
               'tensors': {'weight': {'shape': [1], 'dtype': 'torch.float32'}}}
    hashes = {}
    for phase in ('initial_adapter', 'checkpoint'):
        folder = root / phase
        folder.mkdir()
        (folder / 'adapter.safetensors').write_bytes(data)
        (folder / 'manifest.json').write_bytes(encoded(adapter))
        hashes[phase] = {p.name: sha(p.read_bytes()) for p in folder.iterdir()}
    optimizer = root / 'optimizer_state.pt'
    optimizer.write_bytes(b'opaque optimizer bytes never loaded')
    manifest = {'base_pin': BASE, 'checkpoint': str(root / 'checkpoint'),
                'optimizer': str(optimizer), 'optimizer_sha256': sha(optimizer.read_bytes()),
                'initial_files_sha256': hashes['initial_adapter'],
                'checkpoint_files_sha256': hashes['checkpoint']}
    path = root / 'TRAINING_MANIFEST.json'
    path.write_bytes(encoded(manifest))
    return path

class CapsuleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.a = branch(self.root / 'control')
        self.b = branch(self.root / 'candidate')
        self.out = self.root / 'capsule.tar.gz'

    def test_roundtrip_deterministic_and_no_sources_changed(self):
        before = {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        receipt = build_adapter_capsule(self.a, self.b, self.out)
        self.assertEqual(receipt['members'], 13)
        self.assertEqual(verify_adapter_capsule(self.out)['status'], 'verified')
        second = self.root / 'second.tar.gz'
        build_adapter_capsule(self.a, self.b, second)
        self.assertEqual(self.out.read_bytes(), second.read_bytes())
        for p, raw in before.items():
            self.assertEqual(p.read_bytes(), raw)
        with tarfile.open(self.out) as tf:
            names = tf.getnames()
            self.assertEqual(len(names), 13)
            self.assertFalse(any('cache' in x or x.startswith('/') or '..' in x for x in names))

    def test_existing_destination_untouched(self):
        self.out.write_bytes(b'original')
        with self.assertRaises(FileExistsError):
            build_adapter_capsule(self.a, self.b, self.out)
        self.assertEqual(self.out.read_bytes(), b'original')

    def test_missing_candidate_no_output(self):
        with self.assertRaises(ValueError):
            build_adapter_capsule(self.a, self.root / 'absent', self.out)
        self.assertFalse(self.out.exists())

    def test_source_tamper_no_output(self):
        (self.b.parent / 'optimizer_state.pt').write_bytes(b'tampered')
        with self.assertRaises(ValueError):
            build_adapter_capsule(self.a, self.b, self.out)
        self.assertFalse(self.out.exists())

    def test_shape_and_nonfinite_rejected(self):
        raw = tensor(float('nan'))
        manifest = {'sha256': sha(raw), 'tensors': {'weight': {'dtype': 'torch.float32', 'shape': [1]}}}
        with self.assertRaisesRegex(ValueError, 'nonfinite'):
            validate_adapter(raw, manifest)
        raw = tensor()
        manifest['sha256'] = sha(raw)
        manifest['tensors']['weight']['shape'] = [2]
        with self.assertRaisesRegex(ValueError, 'shape'):
            validate_adapter(raw, manifest)

    def test_archive_tamper_unsafe_and_duplicate_rejected(self):
        build_adapter_capsule(self.a, self.b, self.out)
        with tarfile.open(self.out) as tf:
            files = [(x.name, tf.extractfile(x).read()) for x in tf]
        for variant in ('tamper', 'unsafe', 'duplicate', 'symlink'):
            buffer = io.BytesIO()
            with tarfile.open(fileobj=buffer, mode='w:gz') as tf:
                for name, data in files:
                    if variant == 'tamper' and name.endswith('optimizer_state.pt'):
                        data += b'x'
                    info = tarfile.TarInfo(name)
                    info.size = len(data)
                    tf.addfile(info, io.BytesIO(data))
                if variant != 'tamper':
                    info = tarfile.TarInfo('../outside' if variant == 'unsafe' else files[0][0])
                    if variant == 'symlink':
                        info.type = tarfile.SYMTYPE
                        info.linkname = '/etc/passwd'
                    tf.addfile(info)
            buffer.seek(0)
            with self.subTest(variant=variant), self.assertRaises(ValueError):
                verify_adapter_capsule(buffer)

if __name__ == '__main__':
    unittest.main()
