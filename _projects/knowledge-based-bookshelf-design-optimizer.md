---
layout: project
title: "Knowledge-Based Bookshelf Design Optimizer"
description: "A knowledge-based engineering system that automatically designs and optimizes bookshelves by balancing structural safety, cost, and manufacturability using a genetic algorithm and a semantic knowledge base."
hero_image: /assets/images/projects/knowledge-based-bookshelf-design-optimizer/hero.png
tools: ["Python", "Genetic Algorithms", "OWL/RDF (Jena Fuseki)", "FreeCAD", "SPARQL"]
category: "python"
date: 2025-11-09
---

## Overview
This project implements a full KBE system for parametric bookshelf design, where user-defined requirements are optimized using a genetic algorithm. The system integrates structural analysis, cost estimation, manufacturability checks, CAD generation, and a semantic knowledge base. Developed as an individual coursework project in automation for engineer-work.

## Key Visuals

<figure class="project-visual">
  <img src="/assets/images/projects/knowledge-based-bookshelf-design-optimizer/visual-1.png" alt="User interface showing input parameters, 3D-visualisation, and component list.">
  <figcaption><strong>Result:</strong> User interface showing input parameters, 3D-visualisation, and component list.</figcaption>
</figure>

<figure class="project-visual">
  <img src="/assets/images/projects/knowledge-based-bookshelf-design-optimizer/visual-2.png" alt="System architecture diagram showing data flow between WebApp, GA, Analysis, CAD, and Knowledge Base.">
  <figcaption><strong>Process:</strong> System architecture diagram showing data flow between WebApp, GA, Analysis, CAD, and Knowledge Base.</figcaption>
</figure>

<figure class="project-visual">
  <img src="/assets/images/projects/knowledge-based-bookshelf-design-optimizer/visual-3.png" alt="UML class diagram illustrating system architecture and separation of concerns.">
  <figcaption><strong>Analysis:</strong> UML class diagram illustrating system architecture and separation of concerns.</figcaption>
</figure>

## Key Takeaways
<ul class="project-takeaways">
  <li>Achieved automated trade-off optimization between cost, strength, and manufacturability using a GA with constrained design variables.</li>
  <li>Designed a modular architecture separating domain logic, analysis, optimization, CAD, and knowledge-base layers for extensibility.</li>
  <li>Enabled design reuse and component allocation through an OWL/RDF knowledge base queried with SPARQL.</li>
</ul>
