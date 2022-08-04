# Five(Six) Clique

A solution to the problem of finding five English words with 25 distinct characters, using graph theory.

## Description

This is improvement of [solution from Benjamin Paassen](https://gitlab.com/bpaassen/five_clique) that decreases the time needed further down from ~21m to ~10.5s.

## Method

My solution uses finding clique in the graph as Benjamin Paassen does. But the improvment is that in every step we only choose words that contain the most uncommon and unused letter. This is possible due to the fact that all letters have to be used at some point except one. I solved this issue by add all single letter words and I am finding six-clique instead of five-clique.

"But Parker gave it a go. And that's something." ~ Benjamin Paassen

## Quickstart guide

1. Download the `words_alpha.txt` file from https://github.com/dwyl/english-words (this is the same file that Parker used).
3. Run the `savlik_clique.py` file.
