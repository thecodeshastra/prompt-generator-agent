# Trustworthy GenAI

##

### 1. The Core Philosophy: Augmented Intelligence

- Navigation vs. Generation: Do not use GenAI to generate facts; use it to navigate to them. Instead of asking the AI for an answer, ask it where in a specific document or app that answer can be found.
- Hallucination as a Feature: Hallucination is a "bug" for factual tasks but a "feature" for creative work like brainstorming, poetry, or storytelling.
- Output as a "Draft": Treat every AI response as a starting point or a "first draft" that must be fact-checked, edited, and improved by a human expert.

### 2. The ACHIEVE Framework for Trustworthy Use

This framework helps identify appropriate ways to leverage AI while keeping the human in the loop:

- A: Aiding Human Coordination: Use AI to summarize meetings, identify ambiguities in plans, or list follow-up items.
- C: Cutting Out Tedious Tasks: Use it for repetitive work like categorizing free-text survey responses into groups.
- H: Helping Provide a Safety Net: Ask the AI to review your work for errors, such as finding undefined technical terms in a presentation or identifying conflicting decisions between two different teams.
- IEV: Inspiring Better Problem Solving: Use AI to spark imagination or look for new perspectives (e.g., "Act as a skeptic and find flaws in my assumptions").
- E: Enabling Great Ideas to Scale: Use it to expand a single idea into many variations, such as creating personalized email prompts for dozens of different departments.

### 3. Practical Techniques for Reliability

- The Cost of Checking: Only use AI for tasks where the cost of checking the answer is lower than the cost of producing it yourself. For example, AI is great for solving a crossword (easy to verify), but bad for translating rare ancient scripts (hard to verify).
- Filtering and Traceability: Filtering is one of the safest operations because the output is a subset of the input. Always enforce traceability by requiring the AI to provide line numbers, IDs, or direct quotations to support its claims.
- Flipped Interaction: If the user doesn't know what info is needed, instruct the AI to ask the user questions until it has enough context to solve the problem.
- Alternative Approaches: If an answer is unclear due to policy ambiguity, instruct the AI to suggest "alternative approaches" that are clearly allowable instead of guessing the right answer.

### 4. Where to Use Trustworthy GenAI

You can use these principles in various high-value, low-risk scenarios:

- Internal Support Systems: Building custom GPTs for accounting, HR, or policy questions where the AI can provide direct quotes from internal manuals.
- Education and Training: Creating learning aids that explain complex concepts using analogies (e.g., explaining "attention" in AI to a finance professional).
- Safe Navigation in Apps: Enhancing mobile apps (like healthcare portals) so users can ask "Where is my last lab result?" and the AI navigates them to the correct screen instead of reciting the data.
- Adversarial Testing: Before releasing a GPT to the public, use these principles to "Red Team" or attack it to see if it can be tricked into making inappropriate promises or unethical statements.

### 5. When to AVOID Using GenAI

- High-Risk Decision Making: Avoid tasks involving a high risk to human life, health, or legal reputation (e.g., asking if a medication is safe).
- Unverifiable Expertise: If you lack the expertise to evaluate the output, using the AI is a risk. You must be able to perform a "code review" or "policy check" on everything it produces.
