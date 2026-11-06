# Scheme command calibration: primary-source notes

Research date: 2026-11-06. Scope: the fixed SmolLM2-135M-Instruct checkpoint plus the existing local readout LoRA, following the reported 0/10 strict-command result. No model downloads, training, or primary implementation changes were performed. The recommendations below are experiment-design inferences, not established results for this checkpoint.

The present result establishes failure on those ten prompts under that interface. It does not separate token formatting, copying, command selection, argument binding, adapter interference, and semantic execution. None of the sources below establishes Scheme competence in this 135M model.

## 1. Checkpoint-specific official evidence

[HuggingFaceTB/SmolLM2-135M-Instruct model card](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct), Model Summary, How to use, Evaluation, Limitations.

**Read depth:** inspected the actual card, including its training summary and inference examples, rather than relying on the repository name or a converted checkpoint. The card describes SFT followed by DPO. Its function-calling statement explicitly qualifies support as being for the **1.7B** model. Its official usage applies the tokenizer's chat template. Thus the 135M “Instruct” designation supplies no checkpoint-specific promise of function calling, much less a new Scheme protocol.

**Useful control:** keep weights fixed and test the checkpoint's actual tokenizer/template before interpreting command failures as capability failures. Compare plain English response, exact literal copying, and Scheme command selection separately.

**Limit:** the card is a model-release description, not an experiment showing that 135M cannot call tools. Its broad instruction-following evaluations do not validate this local adapter or command vocabulary.

## 2. Serialization and continuation are part of the interface

[Hugging Face Transformers: Chat templates](https://huggingface.co/docs/transformers/en/chat_templating), “Using apply_chat_template,” “add_generation_prompt,” and “continue_final_message.”

**Read depth:** read explanations and API examples, including token duplication and assistant-prefill behavior. Chat models continue token sequences; role boundaries and the assistant-generation marker affect what sequence they continue. The docs advise avoiding duplicated special tokens when separately tokenizing rendered templates. They distinguish starting an assistant turn from continuing an existing assistant prefix; those two options should not be combined.

**Useful control:** record rendered prompt text, final prompt tokens, generated suffix, stop reason, and token budget. Use the model's own template with an assistant boundary as one condition. Treat a supplied `(` or `(command ` assistant prefix as a separate continuation condition.

**Limit:** this is implementation documentation, not a guarantee that template correction or prefilling reveals hidden reasoning. A prefix provides part of the answer; report exactly how much it supplies. Verify behavior against the installed Transformers version.

## 3. Grammar constraints reduce an output space

[Geng et al., EMNLP 2023: Grammar-Constrained Decoding for Structured NLP Tasks without Finetuning](https://aclanthology.org/2023.emnlp-main.674.pdf).

**Read depth:** inspected §§2.1–3.4 and experimental results, including input-dependent entity candidates, parsing validity, and model sizes. The method filters token continuations through a grammar. Evaluations use LLaMA/Vicuna models of 7B–33B, not tiny SmolLM2. Entity disambiguation can constrain outputs to input-specific candidate sets; parsing reports structural validity separately from bracketing F1. The paper also discusses tokenizer-dependent grammar limitations. The authors' [GitHub repository](https://github.com/epfl-dlab/GCD) was verified through the GitHub connector; no code was executed.

**Useful control:** report unconstrained strict accuracy, parse validity, correct command, correct arguments, and final execution/result separately. A syntax-only grammar should retain wrong but legal commands and arguments. A candidate-list grammar is an additional condition because it supplies task information.

**Limit:** a grammar that admits only the gold command makes correctness a property of the harness. Even a useful constrained result demonstrates the combined system. It does not show that grammar forcing creates reasoning, nor does this paper predict gains at 135M.

## 4. LoRA does not make unrelated capabilities invariant

[Biderman et al., TMLR 2024: LoRA Learns Less and Forgets Less, arXiv v2](https://arxiv.org/html/2405.09673v2), §§3–4.2 and Appendix A setup.

**Read depth:** examined datasets, evaluation definitions, rank conditions, and learning/forgetting results. Their principal experiments adapt Llama-2-7B on code/math, with ranks 16/64/256 and all transformer modules targeted. Target-domain learning and source-domain retention are separately measured. Low-rank LoRA often learns less than full fine-tuning while retaining more measured source performance; “less forgetting” does not mean no forgetting.

**Useful control:** compare the existing adapter enabled/disabled using identical prompts, tokenizer, decoding, and limits, without training anything. Measure both Scheme probes and an existing readout sentinel. A Scheme decline with adapter enabled is evidence of behavioral interference under this interface; unchanged failure cannot locate its cause.

**Limit:** this paper neither studies this readout adapter nor establishes a mechanism for its failures. Different model scale, training distribution, ranks, and target modules prevent transferring its numerical results. The prior local adapter was trained for readout, not Scheme.

## Minimal discriminating controls

These are proposed controls, not literature claims or completed measurements:

1. **Copy:** ask for one explicitly supplied complete command, byte-for-byte. Include unfamiliar argument strings. Passing measures reproduction under an instruction, not command selection.
2. **Choose:** provide two legal commands with identical argument types and ask for the one matching a simple request. Swap their order and use held-out values. Passing adds selection evidence beyond copying.
3. **Bind:** supply the command name but require arguments from the request; swap two values in paired requests. Passing adds evidence of argument binding.
4. **Compose:** require selecting and filling the command without an answer-bearing example. Reserve a small untouched set after prompt calibration.

Run only the necessary interface/adapter comparisons first. Keep strict scoring unchanged; additionally diagnose wrapper text, malformed syntax, wrong command, wrong argument, and truncation. If syntax-only constraints are later tested, publish both constrained and unconstrained results and count supplied prefixes/candidates explicitly. Ten failures justify diagnosing this setup; they do not justify a universal claim about tiny models or a claim that a new prompt has succeeded before held-out evaluation.
