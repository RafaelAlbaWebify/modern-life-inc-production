# Image acceptance rubric — narrative first (2026-10-26)

The primary purpose of an image is to communicate its assigned narrative beat. Do not evaluate image quality as literal prompt compliance.

## BLOCKER
Reject or repair when: main character unrecognizable; action contradicts narration's core meaning; major unintended people or props confuse narrative; unreadable generated text distracts viewers; serious anatomy/artifacts; format cannot be used. Verify against actual script, not invented requirements.

## REPAIRABLE
Accept only after localized repair if straightforward: gibberish speech bubbles, stray artifacts, small inappropriate background elements. A repair should be preferred over a full generation if it preserves an otherwise effective composition.

## NONBLOCKING
Do not regenerate for: 4 pedestrians instead of 3 when crowd size isn't essential; phone upright instead of face-down when physically putting it aside remains clear; only one mug instead of two when conversation and presence read clearly; split-panel compositions when useful for storytelling; minor color or prop deviations without identity/narrative effect.

## Decision states
ACCEPT, ACCEPT_WITH_MINOR_NOTES, LOCAL_REPAIR, REGENERATE_FOR_BLOCKER, UNSURE. Only REGENERATE_FOR_BLOCKER can authorize GPU retry. UNSURE requires review; do not auto-regenerate.

## Current pilot audit
SC01 accept; SC02 accept (crowd count not material); SC03 requires contextual narrative review (potential phone-in-hand contradiction); SC04 accept; SC05 accept (phone away from desk despite angle/screen); SC06 local repair for gibberish text if present, evaluate interaction separately. Previous 2/6 headline was an overly strict prompt-compliance score, not reliable editorial reject rate.

The original JSON reviewer contract remains incompatible with these states until code migrated. Do NOT blindly import old review result that triggers four GPU retries.
