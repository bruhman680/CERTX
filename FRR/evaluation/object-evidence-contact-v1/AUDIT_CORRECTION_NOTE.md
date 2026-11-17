# Historical audit reconstruction corrected

The first stage2 audit called the live feedback constructor while examining an inherited first reply in a fork now at turn2. That constructor correctly reads current runtime counters during execution, but a historical audit must use the counters at the saved turn. The resulting assertion caught the audit error. Reconstruct the clock from the saved reply after_state when auditing, not the final branch STATE. No runner, model input, raw output, execution event, copied ancestor or call was changed/repeated. The failing audit source is retained.
