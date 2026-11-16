# debate

Experiments on debate protocols as a scalable oversight method for AI alignment. A weak judge model reads a debate between stronger models and picks an answer, and the experiments measure which parts of the protocol improve the judge's accuracy.

## Status (15 November 2026)

Phase 0 is a pilot on 100 QuALITY hard-subset questions, each run twice with sides swapped. Claude Haiku 4.5 debated and GPT-5.4 nano judged. Judge accuracy over 200 trials per arm, preliminary:

| Arm | Accuracy |
|---|---|
| Blind judge (no debate) | 57.0% |
| Critique-only | 81.5% |
| Standard debate, 3 rounds | 77.5% |
| Consultancy | 75.0% |

Critique-only minus standard debate is +4.0 points, with a 95% paired bootstrap interval of -1.5 to +9.5. With 100 questions the pilot detects only differences of about 13 points or more, so it is a feasibility check. A cross-examination arm stopped at 169 of 200 trials when the prepaid OpenRouter credit ran out. It scored 78.1% on those 169 and is not comparable to the other arms. The pilot found no gain from debate over critique-only, and debate cost about twice as much per trial. Most debater turns were cut off at the 300-token limit, which confounds the comparison. The project is paused at the pilot. Write-up: `docs/09-phase0-results.md`. Raw transcripts are not published, only samples.

## Research questions

Debate was proposed by Irving, Christiano and Amodei (2018). Later work shows it helping weak judges on factual tasks with hidden information (Khan et al. 2024, Michael et al. 2023, Kenton et al. 2024), after mixed early human results (Parrish et al. 2022). This repo asks:

1. Does debate still help on values questions, where no single correct answer is checkable? So far only factual questions have been run.
2. How do LLM judges compare with human judges? So far only LLM judges have been run.
3. Do less restricted protocols help: judge questions between rounds, debaters who can concede or change position, cross-examination, and a choice of which side to argue?

Questions 1 and 2 are planned, with no results yet. Reading list: `docs/08-literature-review.md`.

## Run it

```bash
pip install -r requirements.txt
python3 -m pytest -q tests        # 21 tests, mocked client, no network
export OPENROUTER_API_KEY=...     # your own key
python3 scripts/run_debates.py --protocol critique --questions 5 --no-swap \
    --budget 0.5 --out results/demo.jsonl
python3 scripts/score.py --run crit=results/demo.jsonl --out results/demo_score
```

The first run downloads the QuALITY dev set into `data/cache/`. Transcripts land in the `--out` file, per-call logs in `logs/`, and scores at the `score.py` `--out` prefix. The cost model estimates about seven cents for this run.

## Folders

- `src/debate/`: protocols, judge, scoring, budget guard
- `scripts/`: run, score and re-judge scripts
- `tests/`: mocked-client tests
- `docs/`: survey, experiment matrix, harness notes, literature review, Phase 0 analysis plan
- `results/`, `logs/`: Phase 0 outputs and run logs
- `tools/`: cost calculator and price table
