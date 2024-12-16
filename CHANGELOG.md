# Changelog

## Feedback Sources and Fixes

### Milestone 1 Feedback

Feedback from Milestome 1 were:
- Reorganize the project folder structure, specifically analysis notebook (.ipynb or .Qmd or *Rmd) should be in a sub-directory called something sensible, such as analysis, src, notebooks, docs, etc(
    Added it in the second week.
)
- The email under "enforcement" in the CODE_OF_CONDUCT.md should be tied to the team.
- Include the environment.yml file along side the existing conda environment files (We had the file in the first week but deleted it due to a miscommunication, as we thought only the Conda lock file was needed. Later, we added it back into the repo during the second week)
- Fix issues related to figure display (Added an index.html file, which was later replaced with Quarto rendering)
- Many branch names are not meaningful.

All these feedback were raised in this [issue](https://github.com/UBC-MDS/DSCI522-2425-28-rental-bike-prediction/issues/47) and corrected with these set of PRs: 
[PR26](https://github.com/UBC-MDS/DSCI522-2425-28-rental-bike-prediction/pull/26),
[PR36](https://github.com/UBC-MDS/DSCI522-2425-28-rental-bike-prediction/pull/36),
[PR38](https://github.com/UBC-MDS/DSCI522-2425-28-rental-bike-prediction/pull/38), 
[PR50](https://github.com/UBC-MDS/DSCI522-2425-28-rental-bike-prediction/pull/50), 
[PR75](https://github.com/UBC-MDS/DSCI522-2425-28-rental-bike-prediction/pull/75)


### Milestone 2 Feedback

Feedback from Milestome 2 was:
- Fix Docker image tag because tag pulled from image is pinned to latest and this would potentially cause a similar issue as pinning it to latest in the main Dockerfile. We were unable to update the Docker image using the code provided by Daniel and Tiffany. We worked with Daniel to resolve the issue, but were unsuccessful. That's why we are manually updating the image tag.

This feedback was raised in this [issue](https://github.com/UBC-MDS/DSCI522-2425-28-rental-bike-prediction/issues/86) and was fixed with this [PR87](https://github.com/UBC-MDS/DSCI522-2425-28-rental-bike-prediction/pull/87)


### [Peer Review Feedback](https://github.com/UBC-MDS/data-analysis-review-2024/issues/7)
[Peer Review Issue](https://github.com/UBC-MDS/DSCI522-2425-28-rental-bike-prediction/issues/92)

In summary, the peer review feedbacks are as followed:
- Add cross-referencing hyperlinks for figures and tables 
- Add brief description of each figure and table to explain their relevance
- Reduce number of plots by focusing on the most relevant ones and summarizing less critical ones
- Correct grammatical errors for a consistent and professional tone
- Correct incorrect comments in scripts
- Rename LICENSE file to LICENSE.md for better readability (After consulting with the instructor, it was determined that this comment was irrelevant and therefore not addressed)

These feedbacks were raised in this [issue](https://github.com/UBC-MDS/DSCI522-2425-28-rental-bike-prediction/issues/92) and was fixed with these sets of PR: [PR1](https://github.com/UBC-MDS/DSCI522-2425-28-rental-bike-prediction/pull/105), [PR2](https://github.com/UBC-MDS/DSCI522-2425-28-rental-bike-prediction/pull/103), [PR3](https://github.com/UBC-MDS/DSCI522-2425-28-rental-bike-prediction/pull/104), [PR4](https://github.com/UBC-MDS/DSCI522-2425-28-rental-bike-prediction/pull/93)