# Blog draft — Project 1: Docker + GitHub Actions CI with an AI Commit Guardian

_Status: draft, written at the end of Project 1 (14 Nov 2026). To be
published on LinkedIn / the portfolio blog after a final read-through._

## The idea

Most CI pipelines answer one question: does the code work? This one
answers a second question too: is the commit message any good? Every
pull request gets a per-commit score table from a small checker I wrote
— the AI Commit Guardian — and every merge auto-generates a changelog.
The pipeline doesn't just build the app, it teaches the habit of
writing commits people can actually read later.

## What I built

A small Flask app (five endpoints, the largest job it does is echoing
JSON back) packaged in a multi-stage Docker image and tested by
GitHub Actions. The point was never the app — it was the pipeline
around it:

- **Build-and-test** — pytest with coverage reported (77% total).
- **Lint** — ruff (E, F; 88-char lines) and hadolint for the Dockerfile.
- **AI Commit Guardian** — a rule-based Conventional Commits checker
  (score 0–100) that runs on PRs and comments a score table. An
  optional LLM layer (Ollama / OpenAI / Gemini) can improve the
  suggested fix, but it is disabled by default and the rule-based
  checker needs no API key at all.
- **Auto-changelog** — git-cliff when available, a small
  no-dependency Python script as fallback, committed by the CI bot.

## What I learned

- **Docker layering is a design decision, not a copy-paste.** The
  multi-stage build (a `builder` stage that installs dependencies
  into `/install`, then a slim `runtime` stage that copies only the
  packages plus `app/`) is the first time the image structure felt
  deliberate rather than inherited. The trade-off is honest: I
  couldn't measure the size saving locally, because Docker isn't
  installed on my VM — CI is the only proof, and the README says so.
- **CI job design is about feedback speed, not job count.** Splitting
  lint, docker-lint and the commit review into separate jobs means a
  bad commit message fails fast with a readable table, instead of
  hiding inside a monolithic build log.
- **Conventional Commits are a habit, not a format.** Writing 15
  atomic commits for Day 1 forced the discipline: one logical change
  per commit, a message that says what and why. The guardian just
  makes the rule visible — the habit is the actual skill.
- **A fallback is a feature.** The changelog generator has two paths
  (git-cliff, then a plain Python script) and the LLM layer degrades
  to rule-based suggestions when unconfigured. The pipeline works
  with zero keys and zero paid services.

## Challenges

- **Docker wasn't available locally**, so every image change was
  verified in GitHub Actions. That slowed the loop and taught me to
  read CI logs properly instead of assuming the build worked.
- **History divergence.** The first 15 commits were pushed through
  the GitHub web UI because the GitHub App had no write access, so
  the local git history and the GitHub history were different
  objects with identical content. Landing Days 2–7 on top of the
  GitHub state — instead of pushing local history — was the fix,
  and the lesson is to verify what `main` actually is before
  assuming a local branch can be pushed.
- **A week that slipped.** Days 2–3 were built on time but didn't
  land for five days while a go-ahead was unanswered. The work
  survived because it was backed up outside `/tmp` and re-verified
  in a clean venv; the schedule didn't. The fix was a revised plan
  with real dates, not pretending the missed days didn't happen.
- **Measuring honestly.** Coverage is reported, not gated, and the
  LLM module sits at 26% because its providers are disabled by
  default. PR review time is listed as "to be measured" — no
  invented baseline. The numbers in this project are the ones I
  actually ran.

## What's next

Project 2 (Green Deploy Advisor) takes this same app and deploys it
on a free tier, scoring each candidate by cost and carbon. The app,
the guardian and the CI habits all carry forward — that's the point
of the twelve projects being cumulative.
