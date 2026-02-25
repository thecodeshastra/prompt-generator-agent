# Prompt Engineering

Doc Type: Notes
Tags: Agent Prompt, Prompt

## Introduction to prompt engineering

- What it is: Crafting smart instructions (prompts) to make AI give you exactly what you want. It's about clear communication with a powerful, literal assistant.
- Why it Matters: Unlocks AI's full potential, saves time (e.g., writing emails), and gives you control over output style and content.
- Example of prompt

    ```markdown
    Poor Prompt: "Write about dogs"
    Result: Generic, unfocused content about dogs in general
    
    Good Prompt: "Write a 500-word informative article about dog training techniques for first-time puppy owners, focusing on house training and basic commands like sit, stay, and come. Use an encouraging, supportive tone."
    Result: Specific, useful content targeted to the exact audience and purpose
    ```

- A good prompt can consist of 4 key elements - Instructions, Context, Input data and Output indicator.

### Core Principles (Your Golden Rules)

- Be CLEAR & SPECIFIC:
  - Clear: State exactly what you need.
  - Specific: Use precise words, define terms, set boundaries (what NOT to do).
  - *Be explicit, Avoid ambiguity, define terms, set boundaries
- Provide CONTEXT:
  - Background: Give relevant details for the situation.
  - Audience: Who is this for? (e.g., a beginner, your boss).
  - Purpose: Why do you need this?
  - Constraint communication: share limitations or requirements
- STRUCTURE & ORGANIZE:
  - Flow: Present info logically.
  - Format: Use lists, headings, or show examples.
  - Prioritization: put the most important information first
  - Examples: show what good output looks like

### Basic Prompt Structure (Your Recipe) Almost every good prompt needs

- ROLE: Who should the AI act as? (e.g., "You are a marketing expert.")
- CONTEXT: The background or situation.
- TASK: The specific action. (e.g., "Summarize this article.")
- FORMAT: How should the output look? (e.g., "in bullet points," "as a table.")
- TONE: The desired style. (e.g., "professional," "humorous.")
- Template:

    ```markdown
    [ROLE]: Act as [specific role/expert]
    [CONTEXT]: In the context of [situation/background]
    [TASK]: [Specific action or output desired]
    [FORMAT]: Present this as [specific structure]
    [TONE]: Using a [specific style/voice]
    ```

- Practical Example:

    ```markdown
    ROLE: Act as a financial advisor
    CONTEXT: For a 25-year-old recent graduate with student loans
    TASK: Create a beginner's guide to building an emergency fund
    FORMAT: Present as a step-by-step plan with specific dollar amounts
    TONE: Using an encouraging, non-judgmental tone
    ```

### The CLEAR framework

- A systematic approach to prompt construction:

```markdown
**C** - **Context**: Provide relevant background information
**L** - **Length**: Specify desired output length
**E** - **Examples**: Show what good output looks like
**A** - **Audience**: Define who the output is for
**R** - **Role**: Assign a specific persona or expertise to the AI
```

- Framework in Action:

```markdown
CONTEXT: We're launching a new fitness app for busy professionals
LENGTH: Write a 200-word product description
EXAMPLES: Like Apple's clean, benefit-focused product descriptions
AUDIENCE: For tech-savvy working adults aged 25-40
ROLE: Act as a product marketing specialist with fitness industry experience
```

### The problem-solution-benefit structure

```markdown
PROBLEM: [Clearly define what needs to be solved]
CONTEXT: [Provide relevant background and constraints]
SOLUTION REQUEST: [Specify what type of solution you need]
BENEFIT FOCUS: [What outcomes are most important]
FORMAT: [How you want the response structured]
```

### The Audience-Purpose-Action Structure

```markdown
AUDIENCE: [Who will use this information]
PURPOSE: [Why they need it]
ACTION: [What they should be able to do with it]
CONSTRAINTS: [Any limitations or requirements]
SUCCESS CRITERIA: [How to measure if it's working]
```

### Prompt Libraries and Documentation

- Building Your Prompt Library:
  - **Category Organization**: Group prompts by use case or industry
  - **Template Creation**: Develop reusable prompt templates
  - **Performance Tracking**: Note which prompts work best for what purposes
  - **Version Control**: Keep track of prompt iterations and improvements
  - **Sharing**: Document effective prompts for team use
- Template Example:

    ```markdown
    PROMPT TEMPLATE: Competitive Analysis
    PURPOSE: Generate structured competitor analysis
    VARIABLES: [Company Name], [Industry], [Specific Features to Compare]
    STRUCTURE:
    - Act as [Role]
    - Analyze [Company] in [Industry]
    - Focus on [Specific Areas]
    - Present as [Format]
    - Include [Quality Controls]
    ```

- Essential prompting techniques
  - Specificity over generality
  - Context layering - Basic, situation, specific, task
  - Output specification - Format and style specification
  - Constraint setting - Resource, time, scope, quality
- Prompt testing and iteration
  - Testing process
        1. Initial Prompt: Create your first version
        2. Evaluate Output: Assess quality against your criteria
        3. Identify Gaps: What’s missing or could be better?
        4. Refine Prompt: Make specific improvements
        5. Test Again: See if the changes improved results
        6. Document: Keep track of what works
- Common Mistakes to Avoid
  - Vague Instructions: Always be clear and specific.
  - Missing Context: Give all necessary background.
  - Overwhelming Complexity: Break big tasks into smaller ones.
  - Ignoring Output Format: Always specify how you want the answer.
  - No Quality Control: Always check and refine AI's output.

### Essential Techniques (Methods - Your Prompting Toolbox)

### 1. Zero-Shot Prompting

#### What it is

Direct instruction to the model with **no examples**. The model relies on pretraining + instruction tuning to understand the task.

#### When to use

- Simple, well-known tasks (classification, summarization, translation)
- First baseline before adding complexity
- Low token budget
- Avoid for unusual/novel tasks or when mistakes are costly

#### Prompt Templates

```text
Classify the text as Neutral, Negative or Positive.

Text: [input text]
Sentiment:
```

```text
You are a helpful assistant.
Rewrite the following paragraph to be clearer and more concise:

[paragraph]
```

### 2. Few-Shot Prompting

#### What it is

Provide 2–5 **input → output examples** in the prompt, then the new input. The model learns the pattern in-context.

#### When to use

- Zero-shot isn't good enough
- Custom formats, labels, or domain-specific styles
- Need to steer model behavior with concrete examples
- Not ideal for complex multi-step reasoning (use CoT instead)

#### Prompt Templates

```text
Task: Use the new word correctly in a sentence.

Example 1:
Word: "whatpu" (small, furry animal native to Tanzania)
Sentence: We were traveling in Africa and we saw these very cute whatpus.

Example 2:
Word: "farduddle" (jump up and down really fast)
Sentence: [model completes]
```

```text
Label each sentence as Positive or Negative.

This is awesome! // Positive
This is bad!     // Negative
Wow that movie was rad! //
```

**Key insight**: Label space and format matter more than label correctness. Even random labels with consistent format can outperform having no labels at all.

### 3. Chain-of-Thought (CoT) Prompting

#### What it is

Prompt the model to **show intermediate reasoning steps** before the final answer.

#### When to use

- Multi-step reasoning: math, logic puzzles, multi-hop QA
- Need transparent, debuggable reasoning
- Can afford longer outputs
- Overkill for simple lookup tasks

#### Prompt Templates

**Few-Shot CoT**

```text
You are a step-by-step reasoning assistant.

Q: The odd numbers in this group add up to an even number: 4, 8, 9, 15, 12, 2, 1.
A: Adding all the odd numbers (9, 15, 1) gives 25. The answer is False.

Q: The odd numbers in this group add up to an even number: 15, 32, 5, 13, 82, 7, 1.
A:
```

**Zero-Shot CoT-style**

```text
[Question]

Think step by step and explain your reasoning before giving the final answer.
```

### 4. Self-Consistency

#### What it is

Sample **multiple CoT reasoning paths** (temperature > 0), then use **majority voting** on final answers.

#### When to use

- Arithmetic and commonsense reasoning where single CoT is unreliable
- You can afford multiple LLM calls
- Need robustness over a single sample

#### Implementation Pattern (pseudo-code)

```python
answers = []
for _ in range(N):  ## e.g. N = 5–10
    response = llm(cot_prompt, temperature=0.7)
    answer = extract_final_answer(response)
    answers.append(answer)

final_answer = majority_vote(answers)
```

Use your normal CoT prompt; the change is in how you sample and aggregate.

### 5. Generated Knowledge Prompting

#### What it is

Two-stage process:

1. Ask the model to **generate relevant background knowledge**.
2. Feed that knowledge + question back in to get a better answer.

#### When to use

- Commonsense reasoning with frequent confident-but-wrong answers
- Tasks requiring explicit world knowledge and explanations

#### Prompt Templates

**Stage 1 – Generate Knowledge**

```text
Generate relevant background knowledge for this statement:

Input: Part of golf is trying to get a higher point total than others.
Knowledge:
```

**Stage 2 – Answer with Knowledge**

```text
Question: Part of golf is trying to get a higher point total than others. Yes or No?

Knowledge: [generated knowledge]

Explain and Answer:
```

### 6. Meta Prompting

#### What it is

Prompting that focuses on the **structure and syntax** of problems and solutions instead of specific concrete examples.

#### When to use

- You want token-efficient templates that generalize across many instances.
- Building reusable frameworks (math solvers, code helpers, reasoning pipelines).
- Fair model comparison without embedding concrete examples.

#### Prompt Template

**Structure-oriented (instead of many examples):**

```text
Task: For each math problem, follow this structure:
1. Identify the known quantities.
2. Identify the operation needed.
3. Compute the result.
4. Output only the final numeric answer.

Problem: [math question]
Answer:
```

Define similar meta-templates per domain: coding, planning, classification, etc.

### 7. Tree-of-Thoughts (ToT)

#### What it is

Generalization of CoT where the model explores a **tree of reasoning branches** with search (BFS/DFS/beam), self-evaluates thoughts, and backtracks when needed.

#### When to use

- Exploration/planning tasks (puzzles, games, combinatorial reasoning).
- Problems where greedy, single-path reasoning often gets stuck.
- You can afford multiple calls and search overhead.

#### Prompt Template (Simple ToT-style)

```text
Imagine three different experts are answering this question.
All experts will write down 1 step of their thinking, then share it with the group.
Then all experts will go on to the next step, etc.
If any expert realises they're wrong at any point then they leave.

Question: [problem]
```

In an agent system, you typically:

- Generate multiple candidate thoughts per step.
- Ask the model (or a critic) to label them "sure / maybe / impossible".
- Use search over the thought tree (keep good branches, prune bad ones).

### 8. Retrieval-Augmented Generation (RAG)

#### What it is

Combine an external **retriever** (vector DB, search) with a **generator** (LLM). Retrieve relevant docs, then feed them + query to the LLM.

#### When to use

- Knowledge-intensive tasks (QA over docs, websites, internal knowledge).
- Need up-to-date or factual answers.
- Want to reduce hallucinations and avoid retraining the base model.

#### System Overview

1. User query → retrieve top-k documents.
2. Build context = docs + query.
3. LLM answers using only that context.

#### Prompt Template

```text
You are a question answering assistant.
Use ONLY the information in the CONTEXT to answer the QUESTION.
If the answer is not in the context, say "I don't know."

CONTEXT:
[doc 1]
[doc 2]
...

QUESTION: [query]

Answer:
```

### 9. Automatic Reasoning and Tool-use (ART)

#### What it is

Framework where a frozen LLM learns, from demonstrations, to interleave **CoT reasoning and tool calls**. During generation, it pauses at tool calls, integrates tool outputs, and continues.

#### When to use

- Multi-step tasks requiring reasoning + external tools (web search, DBs, calculators, APIs).
- You want zero-shot generalization from a library of demonstrations.
- Need extensible systems (update task/tool libraries instead of retraining models).

#### Demonstration Format

```text
Task: [description]

Thought 1: [reasoning]
Action 1: [ToolName(args)]
Observation 1: [tool output]

Thought 2: [reasoning]
Action 2: [ToolName(args)]
Observation 2: [tool output]

...

Final Answer: [answer]
```

#### Instruction Snippet

```text
Given a new task, decompose it into steps.
Use Thought/Action/Observation format.
Call tools when helpful, wait for their outputs, then continue reasoning.
Finish with a Final Answer.
```

### 10. Automatic Prompt Engineer (APE)

#### What it is

LLM-based framework that automatically **generates and searches over candidate prompts**, selecting the best via evaluation on some examples.

#### When to use

- You want automated prompt optimization instead of manual tweaking.
- You have labeled examples and a scoring metric.

#### Process Flow

1. Provide task description + IO examples.
2. Meta-LLM proposes candidate instructions/prompts.
3. For each candidate prompt: run target LLM on validation set, score performance.
4. Select top-performing prompts; optionally iterate.

#### Meta-Prompt Template

```text
You are a prompt engineer.
Given the task description and example input-output pairs, propose 5 different instructions
that could elicit correct behavior from a language model.
Each instruction should be concise, clear, and general.

Task: [description]

Examples:
[input → output pairs]

Candidate Instructions:
1.
2.
3.
4.
5.
```

### 11. Active-Prompt

#### What it is

Active-learning-style method to build better CoT exemplars: pick **most uncertain questions**, get humans to annotate high-quality CoT for those, and use them as new demonstrations.

#### When to use

- Limited human annotation budget.
- Want a strong, compact set of CoT exemplars for a task.

#### Process Flow

1. Start with zero or a small set of CoT examples.
2. For each training question:
   - Sample multiple answers, compute disagreement (uncertainty).
3. Select top-N most uncertain questions.
4. Ask humans to annotate good CoT for them.
5. Add these to the exemplar pool.
6. Re-prompt or retrain.

High-level: use your annotation budget on the **hardest, most confusing** questions.

### 12. Directional Stimulus Prompting (DSP)

#### What it is

A small **policy LM** is trained (e.g., via RL) to generate a "stimulus" or hint that guides a larger, frozen LLM toward better outputs.

#### When to use

- You have a measurable reward (e.g., summary quality).
- Cannot or do not want to fine-tune the large model directly.

#### System Pattern

1. Policy LM: `hint = policy(context)`.
2. LLM: `(context + hint) → output`.
3. Reward: evaluate output, update policy LM.

#### Prompt Template (LLM sees)

```text
Task: Summarize the following article.

Hint: [generated hint from policy LM]

Article:
[article text]

Summary:
```

### 13. Program-Aided Language Models (PAL)

#### What it is

Model generates **program code** (e.g., Python) as the intermediate reasoning, and you execute it to get the answer. Offloads computation to a reliable runtime.

#### When to use

- Math involving dates, arithmetic, combinatorics.
- Data transformations and symbolic reasoning.
- You can safely run code.

#### Prompt Template

```text
You are a Python reasoning assistant.
Given a question, write Python code that computes the answer.
Store the final result in a variable named `answer`.

Question: Today is 27 February 2023. I was born exactly 25 years ago. What is the date I was born in MM/DD/YYYY?

Code:
```

System then:

- Executes returned code.
- Reads `answer`.
- Returns it as final output.

### 14. ReAct

#### What it is

Prompting pattern interleaving **Thought → Action → Observation**. The model reasons, calls tools, observes results, then continues reasoning until it can finish.

#### When to use

- Knowledge-intensive QA with external tools (search, DB, calculator).
- Decision-making in environments (games, shopping, navigation).
- Agent frameworks where transparency and tool use are important.

#### Prompt Template

```text
Question: [question]

Thought 1: [first step of reasoning]
Action 1: Search[query]
Observation 1: [search result]

Thought 2: [interpret observation, decide next action]
Action 2: Lookup[term]
Observation 2: [result]

...

Thought k: [I can now answer]
Action k: Finish[final answer]
```

#### Typical Actions

- `Search[query]` – external search
- `Lookup[term]` – read specific info
- `Calculator[expression]` – math
- `Finish[answer]` – terminate with final answer

System parses actions, executes tools, and feeds their outputs back as Observations.

### 15. Multimodal CoT

#### What it is

Extend CoT to **multimodal** inputs (text + image). First generate multimodal rationales, then derive the answer from those.

#### When to use

- Visual question answering over diagrams, charts, photos.
- Science/educational questions mixing text and visuals.

#### Prompt Template

```text
You are a multimodal reasoning assistant.

Image: [image]
Question: [question]

First, describe all relevant information you see in the image.
Then, reason step by step combining the image information and the text question.
Finally, give your answer.

Reasoning and Answer:
```

### 16. Graph Prompts

#### What it is

Prompting framework oriented around **graph-structured data** (nodes, edges, attributes) to help LLMs reason about graphs.

#### When to use

- Node/edge/graph classification, link prediction.
- Graph-based recommendations or analysis.

#### Prompt Template (Conceptual)

```text
We are working with the following graph:
- Nodes: [list of nodes with attributes]
- Edges: [list of edges and their types]

Task: Predict the label of node X.

Follow this structure:
1. List the neighbors of node X and their key attributes.
2. Explain how these neighbors and attributes influence X's label.
3. Output only the final label.

Reasoning:
[step-by-step reasoning]

Final Label:
[label]
```

---

## AI agent prompt design

### 1. Prompt = Contract

- A prompt defines **behavior**, not conversation
- Treat the LLM like a **smart but literal worker**
- Clear contract → predictable output

---

### 2. Always Use Structured Prompt Blocks

Never write free-form prompts.

Use fixed sections:

- **Role**
- **Context**
- **Task**
- **Instructions**
- **Output Format**

Structure reduces confusion and randomness.

---

### 3. Role — Define Identity

- Specifies **who the agent is**
- Must be specific

Good:

- “Senior Python software engineer”

Bad:

- “Helpful assistant”

Specific roles → focused behavior.

---

### 4. Context — Set Constraints

- Defines environment and expectations
- Controls style and assumptions

Examples:

- Target skill level
- Coding style
- Best practices

Context keeps responses consistent.

---

### 5. Task — One Responsibility Only

- One agent = one job
- One output per request

Good:

- “Generate exactly one Python function”

Bad:

- “Generate code and explain and optimize”

---

### 6. Instructions — Control Behavior

- Rules are **non-negotiable**
- Keep them short and explicit

Examples:

- “Do not add extra text”
- “Avoid complex constructs”
- “Use inline comments”

Rules reduce hallucination and verbosity.

---

### 7. Output Format — Most Critical

- LLMs naturally over-explain
- Agents must produce **usable output**

Always specify:

- Code only
- JSON only
- No markdown
- No explanations

Output format turns LLM into a system component.

---

### 8. Determinism > Creativity

- Agents need predictability
- Creativity causes instability

Use:

- Clear constraints
- Lower temperature
- Fixed structure

---

### 9. Do NOT Put These in Agent Prompts

- Memory logic (for stateless agents)
- Tool logic
- Multi-step workflows
- Multiple roles
- Emotional language

Workflows belong in code, not prompts.

---

### 10. Prompt Does Not Add Intelligence

- Prompt **controls** behavior
- Intelligence comes from the model

Bad output → fix prompt or system design first.

---

### 11. Agent Prompt Checklist

Before finalizing:

- Is role specific?
- Is there only one task?
- Are instructions strict?
- Is output format explicit?
- Is this reusable?

If yes → good agent prompt.

---

### 12. One-Line Rule to Remember

> Good agent prompts reduce freedom, not increase intelligence.
>
