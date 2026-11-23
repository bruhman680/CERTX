# Rank the two requested answer tokens

The free replies in stage 1 frequently reproduced the row, rambled, or selected an option inside an explanation. Compare the next-token log probabilities for the exact bare strings A and B on the identical 16 prompts. Each must be a single distinct native token. Verify that unrestricted argmax reproduces the archived first token before interpreting the restricted rank. Score the higher of A and B and count rows that pass with both menu orders. An always-A or always-B rank scores 8/16 and passes zero order pairs.

This intervention omits alternative leading whitespaces, longer continuations and a full constrained generation. It diagnoses the relative score of the two bare tokens at the first position. No returned response is rescored as though it had generated a different answer.
