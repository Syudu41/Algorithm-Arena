# Algorithm Arena — Guest Lecture PowerPoint Requirements

Presentation brief · MIS 7623: AI Assisted Application Development · October 29, 2026

Based on our conversations, your earlier lecture notes, the course syllabus, and the decisions we made while developing Algorithm Arena, here is the consolidated presentation brief.

The most important principle: This is not a lecture about sorting algorithms or Manim. It is a lecture about your experience using AI to develop software.

Algorithm Arena exists to make that experience tangible.

## 1. Why Algorithm Arena was created

We need to preserve the reasoning behind the project because it is itself a valuable part of the lecture.

## The evolution of the idea

01

The professor's request

Share your experience with building, testing, and security in AI-assisted development.

02

The original idea

Create visually beautiful mathematical or musical signal animations using Manim.

03

The realization

The application does not need AI features. AI can assist in building an ordinary application.

04

The pivot

Choose algorithm visualization because it makes hidden computational steps understandable.

05

The final concept

Algorithm Arena: interactive sorting visualizations powered by Manim, developed with coding agents.

The project was selected because it offers a compact but complete software-development case study: requirements, architecture, coding, visual rendering, testing, debugging, security, and deployment.

It also naturally incorporates your preference for visual explanations.

One especially valuable lesson from the project: An AI coding agent can implement what you asked for while still missing what you actually wanted. We experienced this as the requirements evolved around GitHub Pages, custom inputs, CMR typography, animation timing, and 3Blue1Brown's visual standard.

That belongs in the presentation as an example of requirements engineering, not as a fabricated software failure.

## 2. What the lecture must accomplish

The professor's exact emphasis was:

> "If you can share your experience of building, testing and security that would be great."

The presentation therefore needs to satisfy the following educational objectives.

| Requirement            | What you should demonstrate                                                                        |
| ---------------------- | -------------------------------------------------------------------------------------------------- |
| AI-assisted building   | How you gave coding agents requirements, reviewed outputs, and refined the implementation          |
| Testing                | How you verified algorithm correctness, handled edge cases, and tested the application             |
| Debugging              | A genuine defect or clearly identified educational failure and the correction process              |
| Security               | Input validation, restricted execution, rendering limits, and responsible use of AI-generated code |
| Human–AI collaboration | What you delegated to AI versus what required your decisions                                       |
| Deployment             | What GitHub Pages hosts and why dynamic Manim rendering requires a separate service                |
| Reflection             | Benefits, limitations, failures, and lessons learned                                               |

The October 29 course syllabus also covers multi-agent software workflows. We can connect that topic to planning, coding, testing, and review roles without pretending Algorithm Arena itself contains AI agents.

## 3. Presentation philosophy and visual requirements

Your reference is Shayne Longpre's MIT dissertation defense, combined with the mathematical visualization philosophy associated with Grant Sanderson.

You want the audience to understand the explanation by looking at the screen while you speak—not by reading a slide full of text.

[GitHub - far1din/manim: Manim code](https://images.openai.com/static-rsc-4/7rhBZ7EnpT_amO_wYxQPZnohaJvWCnktGjpkY0_lMM-CO2CCm2G3zHYiLEO3tAVRhTzXP-2xZlSb7beJj-VVD92Uf9R6Au7p6NFQFF2ewPf6V4r53j_nwx-Yq7JWLafRtAn7ZSH9PYk-uSTadm7DtL_kL8S-AKUp4L_lSJJ4oM4?purpose=inline)

Visual explanations

Use mathematical animation and progressive diagrams to make ideas visible.

[Catching up on the weird world of LLMs](https://images.openai.com/static-rsc-4/2LxI0dy_N_1aNwpoxFW_BEVE9lm20VL7kI027g_pvS700M_-i4VN_NOxmPb9-jgwHZK-JJrVb52De8-tZYE5H12Jr_Mxzk1Z0GFa60UI09vQ1JZY_2zke2U5jMwwBOoB73lshY1-yBy9DzcRpADhjj6jwlkNnTUy4LtN8RtZ8FU?purpose=inline)

Minimal typography

One key statement per slide, with very limited supporting text.

[Workflow Kit | Build User-Defined Workflows - Inngest Docs](https://images.openai.com/static-rsc-4/NJp-2eWFWxxMJzHwClWaWn_RXPA_ayuR8JhIo-rTONeZp5A6r-yVPZPEfYcPoP41UW_hHkVxn3L6f7fTyTsq7sXWi81bJZab8SGFWMAg1mK0_0IuqFAf8jHSWeGX6GQN2J7SqHBqnMkjypkpChZJHjJXGvzqJS5cDykvlom_i8Y?purpose=inline)

Architecture as a picture

Explain how components work together without overwhelming students with code.

[Genflow | Sidekick](https://images.openai.com/static-rsc-4/CsQagYjrLwcFvCP1NT32TfDZ-j5B-QRPxjyPvyOmUx0o3wIkZ6wDG_tW2CgwvGyMug-rc-6bZmZaqi-DDqdo5EhoE9OlHEo6-TOUXbqyiTjzePqM8IwgWZ8QmwMSidhA5BVA77Y2T9PfCVG91iR2fQKKBH7R9-37dDkPoHYofhs?purpose=inline)

Evidence over decoration

Use real screenshots, code diffs, tests, and demonstrations from Algorithm Arena.

Design standards:

- 16:9 widescreen, consistent visual identity and high contrast.
- Approximately 15–18 slides for the full lecture, with minimal text.
- Use animation frames, process diagrams, architectural visuals, and genuine development artifacts.
- Show an idea progressively when that helps understanding.
- Keep detailed speaking points separately from slide content.
- Avoid generic AI robot imagery, excessive code screenshots, and fabricated metrics.
- Use Computer Modern Roman where it contributes to the mathematical visual identity; maintain readability elsewhere.

The proposed opening line, "What if we could see how an algorithm thinks?", is our own wording, not a verified quotation from 3Blue1Brown.

## 4. Mandatory AI-assisted development workflow slide

You specifically asked for the entire workflow on one slide. It should be a centerpiece of the presentation.

REQUIRED SINGLE-SLIDE DIAGRAM

## From Idea to Reliable Software

A simplified visual layout. The PowerPoint should also illustrate that failed tests or reviews can send development back to earlier stages.

The audience should understand that AI assistance extends beyond code generation, and that the developer remains responsible for reviewing the work.

## 5. Proposed narrative and slide sequence

Rather than building the deck as a conventional academic lecture, I'd organize it as a story.

| Slides | Story                                                                | Visual treatment                                |
| ------ | -------------------------------------------------------------------- | ----------------------------------------------- |
| 1–2    | Why visualize? Introduce the philosophy and show a Manim animation   | Full-slide animation and one opening question   |
| 3      | Why Algorithm Arena? Explain the original problem and product choice | Idea-evolution diagram                          |
| 4      | What is AI-assisted development?                                     | One lifecycle diagram                           |
| 5–6    | From requirements to architecture                                    | Prompt snippets, UI map, architecture           |
| 7–9    | Building the application                                             | Real development snapshots and live app         |
| 10–12  | Testing and debugging                                                | Edge cases, failed test, code fix, passing test |
| 13–14  | Security and deployment                                              | Trust boundaries and actual safeguards          |
| 15–16  | Lessons learned                                                      | What AI handled and what you verified           |
| 17–18  | Closing and discussion                                               | Three takeaways and Q&A                         |

This is a proposed storyboard, not yet a finished slide deck.

The testing section should receive more emphasis than the explanation of Bubble Sort itself.

## 6. Live demonstration requirements

The prototype is not a decorative accompaniment. It is evidence for the lecture.

The demo should show the actual Algorithm Arena website, navigate from About to Sorting and Bubble Sort, play a genuine pre-generated Manim explanation, and then demonstrate a custom-input workflow if the rendering service is functioning.

The development demonstration should additionally include a real test run, a reproducible defect or clearly disclosed educational baseline, and a security control that is actually implemented.

A crucial distinction from our notes: GitHub Pages cannot run Python/Manim itself. If public custom rendering is unavailable, use the verified local rendering service and clearly explain the difference.

Have recorded backup footage and prepared test outputs so the lecture remains coherent even if live rendering encounters delays.

## 7. Timing and preparation constraints

Provisional 60-minute lecture

Opening and purpose

5m

Development lifecycle

10m

Requirements and architecture

10m

Live prototype

10m

Testing, debugging and security

17m

Lessons and Q&A

8m

Prepare a separate 30-minute fallback. The guest lecture's actual duration is still assumed rather than confirmed.

The deliverables need to be finished by Monday, October 26, to leave Tuesday and Wednesday for your midterm preparation. On Thursday, October 29, your midterm runs from 2:40–4:00 PM and your guest lecture starts at 5:30 PM.

We should not schedule substantial development or slide writing on lecture day.

## 8. What the lecture should avoid

There are several directions that would weaken the presentation.

First, don't turn it into a tutorial on Bubble Sort, Manim, React, or Python. The audience needs enough technical context to understand your decisions, but the focus must remain AI-assisted development.

Second, don't portray AI as having autonomously built a production-ready application. We should show actual prompts, revisions, corrections, and limitations.

Third, don't invent mistakes, testing outcomes, security achievements, or development metrics. Planned examples must be replaced with verified evidence before presentation.

Finally, don't overcrowd the slides. The presenter should provide the explanation, with the visual acting as a clear anchor.

## 9. The key messages the audience should remember

PROPOSED CLOSING SLIDE

# AI accelerates development.

# Requirements shape the result.

# Testing and judgment build trust.

Algorithm Arena is the example. Responsible AI-assisted software engineering is the lesson.

I would make this the guiding brief for the deck.

There is one especially strong and authentic angle here: the evolution of Algorithm Arena is as instructive as the application itself. Your progression from an initially broad Manim concept to a concrete website, and the corrections you had to make to its requirements, demonstrate that using a coding agent doesn't eliminate the need to think like a software engineer.

That story connects the visual opening, your actual development experience, the professor's requested topics, and the final takeaway—without making the lecture unnecessarily technical.