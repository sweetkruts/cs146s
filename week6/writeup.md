# Week 6 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **William Li** \
SUNet ID: **willyli** \
Citations:
- [Semgrep Documentation](https://semgrep.dev/docs/)
- [OWASP SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [OWASP XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [FastAPI CORS Security](https://fastapi.tiangolo.com/tutorial/cors/)

This assignment took me about **1** hours to do. 


## Brief findings overview 
> Semgrep identified 41 total findings across three categories:
>
> **SAST (Static Application Security Testing):** 19 code findings
> - SQL injection vulnerabilities (8 findings) - unsafe string interpolation in SQL queries
> - Code injection (eval usage) - 2 findings
> - Command injection (subprocess with shell=True) - 2 findings
> - Path traversal - 1 finding
> - CORS wildcard policy - 1 finding
> - XSS vulnerabilities (innerHTML with user data) - 1 finding
> - Insecure hash (MD5) - 1 finding
> - Dynamic URL usage - 1 finding
> - SQLAlchemy text() usage - 1 finding
> - Other audit findings - 1 finding
>
> **SCA (Software Composition Analysis):** 22 supply chain vulnerabilities
> - 1 reachable finding (HIGH): Werkzeug CVE-2024-34069
> - 13 undetermined findings (MODERATE): Various CVEs in pydantic, requests, jinja2, werkzeug
> - 8 unreachable findings (including CRITICAL PyYAML vulnerabilities)
>
> **Secrets:** 0 findings (no secrets detected)
>
> **False Positives/Noisy Rules:**
> - The SQLAlchemy ORM queries flagged for SQL injection (lines 33 in action_items.py and notes.py) are false positives. These use SQLAlchemy's safe ORM methods (`.where()`, `.contains()`) which automatically parameterize queries. Semgrep's taint analysis doesn't recognize that ORM methods are safe.
> - The debug endpoints (`/debug/eval`, `/debug/run`, `/debug/read`, `/debug/fetch`) are intentionally insecure for demonstration/testing purposes. They're marked with `# noqa` comments and were ignored for this assignment as they're not production endpoints.
> - Some supply chain findings are "unreachable" meaning the vulnerable dependencies aren't actually used in the code paths, but still present security risk.

## Fix #1
a. File and line(s)
> `backend/app/routers/notes.py`, lines 69-95 (function `unsafe_search`)

b. Rule/category Semgrep flagged
> `python.sqlalchemy.security.audit.avoid-sqlalchemy-text.avoid-sqlalchemy-text`  
> `python.fastapi.db.generic-sql-fastapi.generic-sql-fastapi`  
> `python.tars.fastapi.sql.aiosqlite.fastapi-aiosqlite-sqli`

c. Brief risk description
> **SQL Injection Vulnerability (CRITICAL):** The function uses f-string interpolation directly in SQL text, allowing attackers to inject malicious SQL code. An attacker could execute arbitrary SQL commands to read, modify, or delete data, or potentially gain system access. Example attack: `q = "test' OR '1'='1"` would modify the query logic.

d. Your change (short code diff or explanation, AI coding tool usage)
> Changed from unsafe f-string interpolation to parameterized query:
> ```python
> # BEFORE (vulnerable):
> sql = text(f"WHERE title LIKE '%{q}%' OR content LIKE '%{q}%'")
> rows = db.execute(sql).all()
>
> # AFTER (secure):
> sql = text("WHERE title LIKE :pattern OR content LIKE :pattern")
> safe_pattern = f"%{q.replace('%', '%%').replace('_', '__')}%"
> rows = db.execute(sql, {"pattern": safe_pattern}).all()
> ```
> Used Claude Code to implement parameterized queries with proper wildcard escaping.

e. Why this mitigates the issue
> **Parameterized queries** separate SQL structure from data, preventing injection. SQLAlchemy treats the `:pattern` placeholder as a parameter, not code. User input is properly escaped (replacing SQL wildcards `%` and `_` with `%%` and `__`), then passed as data. Even if an attacker sends `' OR '1'='1`, it's treated as literal text to search for, not executable SQL code. This is the standard OWASP-recommended approach for preventing SQL injection.

## Fix #2
a. File and line(s)
> `backend/app/main.py`, line 24 (CORS middleware configuration)

b. Rule/category Semgrep flagged
> `python.fastapi.security.wildcard-cors.wildcard-cors`

c. Brief risk description
> **Insecure CORS Policy (HIGH):** The wildcard `allow_origins=["*"]` allows any website to make requests to the API, enabling Cross-Site Request Forgery (CSRF) attacks. An attacker's website could send authenticated requests on behalf of users, accessing or modifying their data. This is especially dangerous when combined with `allow_credentials=True`.

d. Your change (short code diff or explanation, AI coding tool usage)
> Restricted CORS to specific allowed origins instead of wildcard:
> ```python
> # BEFORE (insecure):
> allow_origins=["*"],
> allow_methods=["*"],
> allow_headers=["*"],
>
> # AFTER (secure):
> allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
> allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
> allow_headers=["Content-Type", "Authorization"],
> ```
> Used Claude Code to restrict CORS to localhost origins and specify exact methods/headers needed.

e. Why this mitigates the issue
> **Whitelist approach** limits API access to trusted origins only. By specifying exact allowed origins (localhost for development), external malicious websites cannot make cross-origin requests. Explicitly listing required HTTP methods (`GET`, `POST`, etc.) and headers (`Content-Type`, `Authorization`) follows the principle of least privilege—only what's needed is allowed. This prevents unauthorized websites from accessing the API even if a user visits them while authenticated. For production, this should be configured with the actual frontend domain.

## Fix #3
a. File and line(s)
> `frontend/app.js`, line 14 (function `loadNotes`)

b. Rule/category Semgrep flagged
> `javascript.browser.security.insecure-document-method.insecure-document-method`

c. Brief risk description
> **Cross-Site Scripting (XSS) Vulnerability (HIGH):** Using `innerHTML` with user-controlled data (note title and content from API) allows attackers to inject malicious JavaScript code. If an attacker creates a note with HTML/JavaScript payload like `<img src=x onerror="alert('XSS')">`, it will execute when displayed. This could steal authentication tokens, modify page content, or perform actions on behalf of the user.

d. Your change (short code diff or explanation, AI coding tool usage)
> Replaced `innerHTML` with DOM manipulation using `textContent`:
> ```javascript
> // BEFORE (vulnerable):
> li.innerHTML = `<strong>${n.title}</strong>: ${n.content}`;
>
> // AFTER (secure):
> const strong = document.createElement('strong');
> strong.textContent = n.title;
> li.appendChild(strong);
> li.appendChild(document.createTextNode(': ' + n.content));
> ```
> Used Claude Code to implement safe DOM manipulation that treats all content as text, not HTML.

e. Why this mitigates the issue
> **Using `textContent` and DOM methods** ensures all user data is treated as plain text, not HTML/JavaScript. When content is set via `textContent` or `createTextNode()`, the browser automatically escapes special characters (`<`, `>`, `&`, etc.), preventing them from being interpreted as HTML tags or script. Even if an attacker stores `<script>alert('XSS')</script>` as a note title, it will be displayed as literal text, not executed. This follows OWASP's recommendation to use safe DOM APIs that auto-escape content, eliminating XSS risk without needing manual sanitization.