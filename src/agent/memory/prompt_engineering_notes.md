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

1. **Zero-Shot Prompting**
    - This technique involves providing the AI with a task or instruction *without* any preceding examples of input-output pairs. Success relies entirely on the AI’s extensive pre-trained knowledge and the **clarity and specificity** of the prompt itself. To optimize the format, you must explicitly state the purpose, audience, context, and desired output structure.
    - **Example:** *Prompt:* "Write a short paragraph explaining the theory of relativity to a 10-year-old, using analogies from daily life. The output must be exactly four sentences."
2. **Few-Shot Prompting**
    - Few-shot prompting guides the AI by providing 2 to 5 examples of the desired format or behavior before the actual target query. The format structure involves clearly labelled **Input/Output pairs** that demonstrate the pattern you want the AI to follow. This is ideal when the desired style is hard to define purely through text (e.g., highly specific JSON output or a unique writing voice).
    - **Example:**
        - *Input Example 1 (Task):* "The economy grew rapidly."
        - *Output Example 1 (Tone Tag):* Positive
        - *Input Example 2 (Task):* "The results were mixed."
        - *Output Example 2 (Tone Tag):* Neutral
        - *New Task:* "The CEO quit abruptly." (Expected Output: Negative)
3. **Role-Based Prompting**
    - The format requires assigning a specific **persona, expertise level, or professional role** to the AI. This sets the expectation for the tone, vocabulary, and knowledge depth of the response. Effective roles are highly specific (e.g., "Act as a senior data scientist with 10 years in healthcare analytics").
    - **Example:** *Prompt Format:* "**Role:** You are a seasoned investigative journalist focused on tech policy. **Task:** Draft five critical questions to ask a CEO regarding the recent data breach."
4. **Chain-of-Thought (CoT) Prompting**
    - CoT is triggered by instructing the AI to articulate its reasoning process step-by-step *before* delivering the final solution. This is crucial for improving results on complex problems, calculations, or logical reasoning tasks. The instruction is often a specific trigger phrase at the end of the prompt.
    - **Example:** *Prompt Format:* "There are 15 boxes. Each box holds either 5 apples or 8 oranges. If there are 90 pieces of fruit total, how many boxes of apples are there? **Let's break this down into steps.**
        - "Let's think step by step"
        - "Let's work through this systematically"
        - "Let's approach this logically"
        - "Let's break this down into steps"
5. **Meta-Prompting**
    - This involves asking the AI to help improve your original prompt, effectively using the AI as a prompt engineer
    - **Example:** *Act as a Prompt Engineer. Take my prompt below and optimize it for clarity, specificity, and Chain-of-Thought reasoning. Original Prompt: [Your Prompt]*

### Advanced Concepts (Building Complex Workflows)

1. **Iterative Refinement Prompting**
    - This technique recognizes that complex tasks require multiple steps, not one perfect prompt. The format involves a sequence of prompts: **Prompt 1** (Initial Draft) → **Prompt 2** (Specific Feedback/Critique) → **Prompt 3** (Refinement Request). Each subsequent prompt is a concise instruction to fix a known flaw in the previous output.
    - **Example Process:**
        - *P1 (Initial Generation):* "Write a 500-word blog post about climate change solutions."
        - *P2 (Refinement):* "In the previous post, the tone was too academic. **Revise the post to use a more casual, engaging tone, and replace jargon with simpler language.**"
2. **Constraint-Based Prompting**
    - This format uses explicit constraints, acting as guardrails for the model. These constraints can limit the scope, resources used, or quality standards. This improves focus and prevents generic outputs.
    - **Example:** *Prompt:* "Analyze the provided data on Q4 customer churn. (Scope Constraint): **Do not discuss pricing changes; focus solely on user interface friction.** (Quality Constraint): **Ensure the final report adheres strictly to the company's internal formatting guide.**"
3. **Self-Consistency Prompting**
    - This technique is a reliability pattern where the AI is instructed to generate the answer to a complex question **multiple times** (e.g., 3-5 times). The final step requires the AI to synthesize or compare the multiple outputs to arrive at the most consistent and reliable conclusion.
    - **Example:** *Prompt:* "Calculate the total profit margin for all three product lines in 2024. **Generate three separate calculations for verification.** Once complete, present a single synthesized final answer based on the calculation that appeared most frequently."
4. **Prompt Chaining and Workflows**
    - This is a sequential workflow where complex tasks are systematically broken into distinct, focused prompts. The output of the preceding prompt serves as the complete **context and input** for the subsequent prompt. This allows the AI to tackle large, multi-stage projects.
    - **Example (Multi-Stage Research):**
        - *Prompt 1 (Research):* "Identify the three leading competitors for Product X."
        - *Prompt 2 (Analysis):* "Using the list generated in Prompt 1, create a SWOT analysis for each competitor."
        - *Prompt 3 (Synthesis):* "Based on the SWOT analyses from Prompt 2, draft a final recommendation on which competitor poses the greatest threat and why."
5. **Advanced Reasoning (Socratic and Devil's Advocate)**
    - **Socratic Method Prompting:** Uses internal questioning to guide the AI through complex reasoning.
        - *Example:* "Evaluate the ethical dilemma regarding data privacy in this scenario. **First, define the core conflict. Then, identify two possible solutions. Finally, analyze the major flaw in each solution before proposing a final action.**"
    - **Devil's Advocate Prompting:** Instructs the AI to argue against its own initial conclusions.
        - *Example:* "I have concluded that the best material is steel. **Now, argue aggressively as the Devil's Advocate for why aluminum is superior, focusing only on cost and durability.**"
6. **Prompt Programming Patterns**
    - **Conditional Pattern:** This format incorporates IF/THEN logic to handle variations in input or scenario within a single prompt.
    - *Example:* "**IF** the length of the submitted text is greater than 500 words, **THEN** summarize it in three bullet points. **ELSE** if the length is less than 500 words, **THEN** analyze the tone and suggest a title."
7. **Dynamic Context Management**: For long conversations, summarize key points or refresh context periodically so AI doesn't "forget".
8. **Quality Assurance Patterns**: Incorporating techniques like multi-stage validation or "Red Team" reviews where the AI checks its own work or identifies potential issues in its output.
9. **Prompt Optimization Techniques**: Systematically testing different prompt versions (A/B testing) or adjusting prompt elements (parameter tuning) to find the most effective approach.

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