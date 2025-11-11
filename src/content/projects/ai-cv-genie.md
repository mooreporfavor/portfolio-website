---
title: "The 'CV Genie': An AI-Powered Professional Co-Pilot"
client: "Personal Project"
year: 2025
track: "Data Engineering & AI"
tags: ["AI Engineering", "Gemini API", "Serverless Functions", "Python", "Astro", "Prompt Engineering"]
isFeatured: true
---

### Problem

Crafting tailored professional documents, whether a CV for a specific role, a bio for a conference, or a summary for a potential collaborator, is a high-effort, repetitive task. The challenge was to create a tool that could automate and optimize this customization, instantly generating a relevant, high-quality document by leveraging a master vault of my career history.

### Methodology

I designed and built the "CV Genie," a private, AI-native tool integrated directly into my personal website. The project was approached with a bit of levity, framing the tool as a helpful assistant for a common professional chore.

*   **Data Collection & Analysis:** The core knowledge base is a single, exhaustive `CV vault` file, a master "Single Source of Truth" containing every project, skill, and accomplishment (ie. that 10 pages of CV content that should be locked in the vault, but only shared when highly relevant!). During the visioning phase, I used an "Insight-to-Impact Flywheel" framework to map user needs (mine, recruiters, collaborators) against technical feasibility, which led to prioritizing a "Simple Text Prompt" architecture for its immediate utility and low overhead, while also building out more advanced back-end "Pro" model, which is "hidden" to avoid API usage spikes from bots.
*   **Modeling & Technique:** Developed a Python serverless function deployed on Vercel. This function serves as an API endpoint that receives a target context (like a job description or a conference theme) from a hidden front-end page. It then dynamically constructs a detailed prompt, combining the full text of the `CV vault` as context with the target description and a set of instructions. This is then sent to the Google Gemini Pro API to generate the tailored output.
*   **Development & Strategy:** The front-end was built as a simple HTML form on a hidden Astro page. The development was significantly accelerated using Gemini Code Assist as a pair-programmer, particularly for generating client-side JavaScript for the API `fetch` call and debugging the Python serverless function's deployment environment on Vercel.

### Outcome

The CV Genie is a versatile tool that transforms a multi-hour customization task into a 30-second, one-click operation, with utility for a variety of professional stakeholders.

*   **Strategic Impact:** As a "meta-portfolio" piece, the tool tangibly demonstrates an end-to-end implementation of an AI-powered application, showcasing skills in API integration, serverless architecture, and practical prompt engineering.
*   **Utility for Collaborators & Recruiters:** By being built into the website, the tool can be used to instantly generate a tailored bio for a speaking engagement, a short summary for a project proposal, or provide a recruiter with a CV that directly speaks to their specific needs, increasing the speed and relevance of professional interactions.
*   **Knowledge Impact:** The project provided deep, hands-on experience with the common challenges of deploying hybrid Python/Node.js applications to a serverless environment, including managing environment variables