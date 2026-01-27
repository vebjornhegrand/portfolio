---
layout: project
title: "Aerodynamic Performance Prediction from 3D Geometry"
description: "Replaced 24–48h CFD drag-coefficient runs with an instant machine learning surrogate so automotive teams can screen 100+ designs cheaply before doing expensive final CFD validation."
hero_image: /assets/images/projects/aerodynamic-performance-prediction-from-3d-geometry/hero.png
tools: ["Python", "PyTorch", "scikit-learn", "XGBoost", "NumPy"]
category: "python"
date: 2026-01-27
---

## Overview
Built and compared three regression approaches to predict vehicle drag coefficient (Cd) directly from 3D geometry: PointNet on raw point clouds vs. Random Forest and XGBoost on 20 engineered geometric features. The goal was to enable fast design-space exploration by using ML for rapid screening and reserving CFD for final verification.

## Key Visuals

<figure class="project-visual">
  <img src="/assets/images/projects/aerodynamic-performance-prediction-from-3d-geometry/visual-1.png" alt="Predictions versus actual values of the best point cloud model.">
  <figcaption><strong>Result:</strong> Predictions versus actual values of the best point cloud model.</figcaption>
</figure>

<figure class="project-visual">
  <img src="/assets/images/projects/aerodynamic-performance-prediction-from-3d-geometry/visual-2.png" alt="Analysis of the data spread.">
  <figcaption><strong>Analysis:</strong> Analysis of the data spread.</figcaption>
</figure>

<figure class="project-visual">
  <img src="/assets/images/projects/aerodynamic-performance-prediction-from-3d-geometry/visual-3.png" alt="Preprocessing and normalization of the 3D clouds.">
  <figcaption><strong>Process:</strong> Preprocessing and normalization of the 3D clouds.</figcaption>
</figure>

## Key Takeaways
<ul class="project-takeaways">
  <li>Best accuracy: PointNet on point clouds achieved R² = 0.75 and MAE = 0.007, outperforming feature-based baselines.</li>
  <li>Design tradeoff: Direct point-cloud learning beat 20 handcrafted geometry descriptors (bounding box, aspect ratios, convex hull stats), showing the value of learning shape features end-to-end.</li>
  <li>Business impact: Inference is ~10,000× faster and costs fractions of a cent, enabling 100+ design screens and large CFD cost/time savings.</li>
</ul>
