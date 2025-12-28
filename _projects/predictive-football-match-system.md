---
layout: project
title: "Predictive Football Match System"
description: "An end-to-end machine learning system that predicts football match outcomes and evaluates multiple decision strategies through large-scale simulation and optimization."
hero_image: /assets/images/projects/predictive-football-match-system/hero.png
tools: ["Python", "TensorFlow/Keras", "Streamlit", "SQLite", "Genetic Algorithm"]
category: "python"
date: 2025-12-18
---

## Overview
This project implements a production-grade pipeline for probabilistic prediction of Premier League match outcomes using an ensemble of machine learning and time-series models. The predictions are consumed by a simulation engine that evaluates 20 different decision strategies under uncertainty. A genetic algorithm is used to optimize strategy parameters, and system performance is tracked continuously through a live analytics dashboard.

## Key Visuals

<figure class="project-visual">
  <img src="/assets/images/projects/predictive-football-match-system/visual-1.png" alt="Plot of the strategies with the best ROI%">
  <figcaption><strong>Analysis:</strong> Plot of the strategies with the best ROI%</figcaption>
</figure>

<figure class="project-visual">
  <img src="/assets/images/projects/predictive-football-match-system/visual-2.png" alt="Live results of different strategies´performance.">
  <figcaption><strong>Analysis:</strong> Live results of different strategies´performance.</figcaption>
</figure>

## Key Takeaways
<ul class="project-takeaways">
  <li>Built an ensemble prediction system combining deep learning, gradient boosting, and probabilistic models to generate calibrated outcome probabilities.</li>
  <li>Designed a strategy simulation framework that compares risk–reward trade-offs across 20 decision policies using multi-objective optimization.</li>
  <li>Demonstrated that different strategies dominate under different objectives, with one achieving the highest long-term return and another delivering superior risk-adjusted performance.</li>
</ul>
