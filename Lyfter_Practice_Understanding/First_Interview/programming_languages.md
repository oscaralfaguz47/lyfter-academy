# Programming Languages in 2 Cards

The 2 topics: **Interpreted** and **Compiled**.

---

# 1. Compiled

> A **compiler** turns the whole source code into machine code **before** you run it.
> The result is a file the computer can run directly.

```
my_code.c  ->  [ COMPILER ]  ->  program.exe  ->  runs on the CPU
                (before)
```

| Good | Bad |
|---|---|
| Runs fast | You must compile again for each system |
| Errors are caught before running | Slower to write and test |
| No extra software needed to run it | |

**Examples:** C, C++, Rust, Go

---

# 2. Interpreted

> An **interpreter** reads and runs the code line by line **while** the program runs.
> There is no separate file to run.

```
my_code.py  ->  [ INTERPRETER ]  ->  runs line by line
                   (while running)
```

| Good | Bad |
|---|---|
| Works anywhere the interpreter is installed | Runs slower |
| Fast to write and test | Errors only show up while running |
| No compile step | The user needs the interpreter |

**Examples:** Python, JavaScript, Ruby, PHP

---

# Side by side

| | Compiled | Interpreted |
|---|---|---|
| When it translates | **Before** running | **While** running |
| Produces | A runnable file | Nothing |
| Speed | Fast | Slower |
| Errors show up | When compiling | When running |
| Moving to another system | Compile again | Just run it |
| Examples | C, C++, Rust, Go | Python, JavaScript, Ruby |

---

# The bonus point: Python is both

Python is **interpreted**, but there is a step in between:

```
my_code.py  ->  bytecode (.pyc)  ->  [ PVM ]  ->  runs
                 (compiled)         Python Virtual Machine
```

That `__pycache__` folder you see is the bytecode. It is **not** machine code — it is a middle format that the Python Virtual Machine reads.

**Java works the same way:** `.java` -> bytecode `.class` -> the JVM runs it.
**C# too:** `.cs` -> CIL -> the CLR runs it (and turns it into machine code while running).

---

# The line that sets you apart

> Compiled and interpreted describe the **implementation**, not the language itself.

There is nothing in C that says it must be compiled — C interpreters exist.
There is nothing in Python that says it can't be compiled — tools like Nuitka do it.

So the best answer to *"is X compiled or interpreted?"* is:
**"The usual implementation of X is..."**

---

# Cheat sheet

```
COMPILED     -> translated BEFORE running  -> makes a runnable file
                Fast to run, slow to write, must recompile per system
                C, C++, Rust, Go

INTERPRETED  -> translated WHILE running   -> no file produced
                Slow to run, fast to write, works anywhere
                Python, JavaScript, Ruby, PHP

PYTHON       -> interpreted, but compiles to bytecode first (__pycache__)
                then the PVM runs that bytecode
```

---

# Quick self-test

Cover the right column. Answer out loud.

| Question | Answer |
|---|---|
| What is a compiled language? | The whole code is translated into machine code before running, making a runnable file. |
| What is an interpreted language? | The code is read and run line by line while the program runs. |
| Main advantage of compiled? | It runs fast, and errors are caught before running. |
| Main advantage of interpreted? | It works anywhere the interpreter is installed, and it's faster to write and test. |
| Is Python compiled or interpreted? | Interpreted, but it compiles to bytecode first and the Python Virtual Machine runs that. |
| What is `__pycache__`? | The folder where Python stores the bytecode of your files. |
| Give 3 compiled languages. | C, C++, Rust (or Go). |
| Give 3 interpreted languages. | Python, JavaScript, Ruby (or PHP). |
| The bonus answer? | Compiled or interpreted describes the implementation, not the language itself. |