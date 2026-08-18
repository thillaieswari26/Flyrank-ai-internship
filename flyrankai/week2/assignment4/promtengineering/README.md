# Prompt Engineering Iteration Log

## FlyRank AI Fluency — Foundations

**Phase:** Foundations  
**Task:** Debug FastAPI/Uvicorn error

---

## 1. Task

Debug the following error encountered while building a FastAPI Task CRUD API:

```text
Attribute "app" not found in module "main"
````

The command being used was:

```bash
uvicorn main:app --reload
```

The goal was to understand the actual cause of the error rather than simply apply a fix.

---

## 2. Version 1 — Naive Prompt

### Technique

Naive baseline

### Prompt

```text
Why am I getting "Attribute app not found in module main" when running uvicorn main:app --reload?

Explain the cause clearly and show me how to fix it.
```

### Output

This error means Uvicorn cannot find an object named `app` inside your `main` module.

When you run:

```bash
uvicorn main:app --reload
```

Uvicorn interprets this as:

* `main` → the Python module (`main.py`)
* `app` → the FastAPI application object inside `main.py`

Make sure your `main.py` contains:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}
```

Then run:

```bash
uvicorn main:app --reload
```

Also make sure you are running the command from the directory containing `main.py`.

### What Changed and Why

Nothing was added. This was the simple prompt I would have used before learning prompt engineering.

### Observed Difference

The response was correct but generic. It did not know that I was a beginner or that I was working on a Task CRUD API.

---

## 3. Version 2 — Role Assignment

### Technique

Role assignment

### Prompt

```text
Act as an experienced FastAPI backend developer and help me debug this error.

Why am I getting "Attribute app not found in module main" when running uvicorn main:app --reload?

Explain the cause clearly and show me how to fix it.
```

### Output

The error means Uvicorn successfully found `main.py`, but inside `main.py` it could not find a variable named `app`.

When you run:

```bash
uvicorn main:app --reload
```

Uvicorn interprets it as:

* `main` → find `main.py`
* `app` → find the FastAPI object named `app`

Your `main.py` should contain:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello World"}
```

If your application is named something else:

```python
api = FastAPI()
```

then you would need:

```bash
uvicorn main:api --reload
```

### What Changed and Why

I assigned the AI the role of an experienced FastAPI backend developer.

### Observed Difference

The answer became more technically focused and included a realistic example of using a different FastAPI variable name.

---

## 4. Version 3 — Context and Motivation

### Technique

Context and motivation

### Prompt

```text
Act as an experienced FastAPI backend developer and help me debug this error.

I am a beginner learning backend development through a FastAPI internship assignment. I am building a Task CRUD API using FastAPI and Uvicorn. My project uses a file named main.py, and I am trying to start the server locally.

When I run:

uvicorn main:app --reload

I get:

Attribute "app" not found in module "main"

I want to understand the actual cause rather than just apply a random fix, because I am learning FastAPI and need to be able to explain the solution in my assignment.

Explain the cause clearly, show me how to fix it, and explain the important concept I should remember.
```

### Output

The response explained that:

```bash
uvicorn main:app --reload
```

contains two important parts:

* `main` refers to the Python module `main.py`.
* `app` refers to the FastAPI object inside `main.py`.

The error means Uvicorn successfully found and imported `main.py`, but could not find an object named `app`.

The response showed:

```python
from fastapi import FastAPI

app = FastAPI()
```

It also explained that if the application was named:

```python
application = FastAPI()
```

the command would need to use the matching name.

### What Changed and Why

I added my experience level, project context, and motivation.

### Observed Difference

The answer became more relevant to my actual situation and explained the concept in a way that supported my learning goal.

---

## 5. Version 4 — Few-Shot Examples

### Technique

Few-shot examples

### Prompt

```text
Act as an experienced FastAPI backend developer and help me debug this error.

I am a beginner learning backend development through a FastAPI internship assignment. I am building a Task CRUD API using FastAPI and Uvicorn. My project uses a file named main.py, and I am trying to start the server locally.

When I run:

uvicorn main:app --reload

I get:

Attribute "app" not found in module "main"

I want to understand the actual cause rather than just apply a random fix, because I am learning FastAPI and need to be able to explain the solution in my assignment.

Here is an example of the style I find useful:

Example problem:
"Why does Python say NameError: name 'x' is not defined?"

Example useful answer:
"The error means Python reached a line that uses x before x was defined. First identify where x should be created, then make sure it exists before that line runs."

Now explain my FastAPI error in a similar way:
first explain the exact meaning of the error,
then identify the likely cause,
then show a minimal correction,
and finally mention another important cause I should check.

Do not assume that I already understand FastAPI internals.
```

### Output

The response explained that Uvicorn found `main.py` but could not find an object named `app`.

It explained:

```bash
uvicorn main:app --reload
```

as:

* `main` → Python module `main.py`
* `app` → object named `app` inside that module

It provided:

```python
from fastapi import FastAPI

app = FastAPI()
```

and explained that using:

```python
my_app = FastAPI()
```

would cause the error because Uvicorn is looking for `app`.

### What Changed and Why

I provided an example of the desired explanation style.

### Observed Difference

The response followed the requested reasoning pattern more consistently: meaning → cause → correction → additional check.

---

## 6. Version 5 — Output Structure

### Technique

Output structure

### Prompt

```text
Act as an experienced FastAPI backend developer and help me debug this error.

I am a beginner learning backend development through a FastAPI internship assignment. I am building a Task CRUD API using FastAPI and Uvicorn. My project uses a file named main.py, and I am trying to start the server locally.

When I run:

uvicorn main:app --reload

I get:

Attribute "app" not found in module "main"

I want to understand the actual cause rather than just apply a random fix.

Use exactly this structure:

1. ERROR MEANING
- Explain what the error means in simple terms.

2. LIKELY CAUSE
- Explain the most likely cause.

3. FIX
- Give the minimal corrected code and command.

4. OTHER THINGS TO CHECK
- Give up to 3 possible causes.

5. KEY CONCEPT
- Explain what main:app means.

Keep the answer beginner-friendly and concise.
```

### Output

### 1. ERROR MEANING

The command:

```bash
uvicorn main:app --reload
```

tells Uvicorn:

* `main` → find `main.py`
* `app` → find a FastAPI object named `app`

The error means Uvicorn found `main.py`, but could not find an object called `app` inside it.

### 2. LIKELY CAUSE

The most likely cause is that `main.py` does not contain:

```python
from fastapi import FastAPI

app = FastAPI()
```

For example:

```python
my_app = FastAPI()
```

would fail because the object is called `my_app`, not `app`.

### 3. FIX

Use:

```python
from fastapi import FastAPI

app = FastAPI()
```

Then run:

```bash
uvicorn main:app --reload
```

### 4. OTHER THINGS TO CHECK

* Another `main.py` may be getting imported.
* The FastAPI object may have a different name.
* The terminal may be in the wrong directory.

### 5. KEY CONCEPT

`main:app` means:

> Import `main.py` and find the object named `app` inside it.

### What Changed and Why

I explicitly defined the structure of the expected response.

### Observed Difference

The response became easier to scan because each part of the debugging process had a specific location.

---

## 7. Version 6 — Step Decomposition

### Technique

Step decomposition

### Prompt

```text
Act as an experienced FastAPI backend developer and help me debug this error.

I am a beginner learning backend development through a FastAPI internship assignment. I am building a Task CRUD API using FastAPI and Uvicorn. My project uses a file named main.py, and I am trying to start the server locally.

When I run:

uvicorn main:app --reload

I get:

Attribute "app" not found in module "main"

I want to understand the actual cause rather than just apply a random fix.

Debug the problem using this process:

Step 1: Interpret the Uvicorn command and explain main:app.

Step 2: Identify exactly what Uvicorn must find inside main.py.

Step 3: Explain the most likely reason the error occurs.

Step 4: Show the smallest code change needed to fix it.

Step 5: Show the correct Uvicorn command.

Step 6: Give up to three checks if the error still occurs.

Step 7: Finish with the key concept I should remember.

Keep the answer beginner-friendly, practical, and concise.
```

### Output

### Step 1: What `main:app` means

In:

```bash
uvicorn main:app --reload
```

* `main` → the Python module/file `main.py`
* `app` → the FastAPI application object inside `main.py`
* `--reload` → automatically restart the server when code changes

Uvicorn is essentially asking:

> "Open `main.py` and give me the object called `app`."

### Step 2: What Uvicorn must find

The file must contain:

```python
from fastapi import FastAPI

app = FastAPI()
```

The important part is:

```python
app = FastAPI()
```

### Step 3: Why the error occurs

The error:

```text
Attribute "app" not found in module "main"
```

means Uvicorn successfully found and imported `main.py`, but there is no variable/object named `app` inside it.

For example:

```python
my_app = FastAPI()
```

creates an application called `my_app`, but Uvicorn is looking for `app`.

### Step 4: Smallest fix

Change:

```python
my_app = FastAPI()
```

to:

```python
app = FastAPI()
```

### Step 5: Correct command

Run:

```bash
uvicorn main:app --reload
```

from the directory containing `main.py`.

### Step 6: If it still does not work

1. Make sure the file is actually named `main.py`.
2. Make sure `app = FastAPI()` exists at the top level.
3. Make sure Uvicorn is running from the correct folder.

### Step 7: Key concept

```text
uvicorn main:app
        │    │
        │    └── app object inside main.py
        └─────── main.py
```

The `module:attribute` pattern tells Uvicorn which Python module to import and which object inside that module it should serve.

### What Changed and Why

The debugging process was broken into explicit steps.

### Observed Difference

This produced the clearest workflow because the response explained the command, expected object, cause, fix, verification, and key concept in sequence.

---

# 8. Cross-Model Comparison

The final prompt was compared between ChatGPT and Claude.

| Aspect          | ChatGPT               | Claude                    |
| --------------- | --------------------- | ------------------------- |
| Tone            | Beginner-friendly     | More technical            |
| Accuracy        | Correct               | Correct                   |
| Structure       | Clear and organized   | Clear and organized       |
| Explanation     | Simple and accessible | More technically precise  |
| Troubleshooting | Basic checks          | More detailed diagnostics |
| Best strength   | Teaching beginners    | Technical debugging       |

### ChatGPT

ChatGPT provided a beginner-friendly explanation and clearly connected `main:app` to `main.py` and `app = FastAPI()`.

Its main weakness was some repetition.

### Claude

Claude provided a technically precise explanation and gave stronger diagnostic suggestions. It was slightly more technical in wording.

### Conclusion

Both models correctly solved the problem, but they emphasized different strengths.

ChatGPT was more accessible for a beginner, while Claude provided slightly deeper technical troubleshooting.

---

# 9. Final Reusable Prompt Template

```text
Act as an experienced [LANGUAGE / FRAMEWORK] developer and help me debug the following problem.

I am working on [PROJECT / TASK].

The error I encountered is:

[ERROR MESSAGE]

Relevant code or configuration:

[CODE / CONFIGURATION]

Expected behavior:

[EXPECTED BEHAVIOR]

Actual behavior:

[ACTUAL BEHAVIOR]

I want to understand the root cause rather than simply apply a fix.

Debug the problem using this process:

Step 1: Interpret the error and explain exactly what it means.

Step 2: Identify what the program or framework is expecting.

Step 3: Explain the most likely root cause based on the information provided.

Step 4: Show the smallest practical fix, including corrected code where appropriate.

Step 5: Explain how I can verify that the fix worked.

Step 6: Give up to three additional checks if the problem persists.

Step 7: Finish with the key concept I should remember.

Keep the explanation appropriate for my experience level. Clearly distinguish between the confirmed cause and possible alternative causes. Avoid unnecessary information and do not assume facts that I have not provided.
```

---

# 10. Reflection

This exercise showed that prompt engineering is not simply about making prompts longer.

Each technique had a specific purpose:

* **Role assignment** improved technical focus.
* **Context and motivation** made the response more relevant to my situation.
* **Few-shot examples** guided the response style and reasoning pattern.
* **Output structure** made the answer easier to read and evaluate.
* **Step decomposition** created a logical debugging workflow.

The final prompt produced a more controlled, structured, and useful response than the naive prompt.

The main lesson I learned is that an effective prompt should communicate the task, context, desired reasoning process, and expected output clearly instead of relying on the AI to guess what kind of response is needed.

---

# 11. Deliverable Checklist

* [x] Real task selected
* [x] Naive prompt created
* [x] Five additional iterations completed
* [x] Role assignment used
* [x] Context and motivation used
* [x] Few-shot examples used
* [x] Output structure used
* [x] Step decomposition used
* [x] Outputs documented
* [x] Changes and observed differences documented
* [x] Cross-model comparison included
* [x] Reusable prompt template created