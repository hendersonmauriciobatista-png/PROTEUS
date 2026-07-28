# Getting Started With ICFACTORY

This guide is for a technically competent reader who is encountering ICFACTORY for the first time and wants to understand how to begin adoption without direct help from the framework creator.

It does not replace the Constitution, the Governance Architecture, the Constitutional Lexicon or the Project Constitution Template. It only gives the first adoption path.

## Before You Start

You should have:

* a project or system that needs controlled governance;
* a reason to preserve auditability and traceability;
* willingness to separate observation from intervention;
* willingness to identify authority before making structural changes;
* a basic understanding of technical documentation and system architecture.

You do not need to know ACI, CIE-X, ALO, OSE or TUX before starting. Those concepts can be consulted later through the document map.

## What You Will Produce

The first adoption output is not code.

The first output should be a controlled understanding of how your project will relate to ICFACTORY. In practice, that usually means beginning a Project Constitution using:

`governance/PROJECT_CONSTITUTION_TEMPLATE.md`

At the end of this first pass, you should be able to identify:

* what your project is;
* why it needs governance;
* which constitutional principles apply;
* which authorities must be declared;
* which evidence and records will be needed;
* whether the project can begin as draft, non-vigente or approved.

## Step 1 - Understand The Boundary

ICFACTORY is the framework.

Your project is the implementation domain.

H&A is one implementation domain already present in this repository. It is useful context, but it is not required for adopting ICFACTORY elsewhere.

Do not assume that H&A-specific runtime components are mandatory parts of ICFACTORY. The framework is expressed through its constitutional, governance, conceptual and onboarding documents.

## Step 2 - Read The Constitution And Governance Architecture

Read:

1. `CONSTITUTION.md`
2. `governance/GOVERNANCE_ARCHITECTURE.md`

The Constitution explains the principles that cannot be bypassed.

The Governance Architecture explains the relationship between:

1. ICFACTORY Constitution
2. Project Constitution
3. Operational governance layer
4. System

At this stage, do not try to memorize every term. The goal is to understand the direction of authority and why the framework insists on explicit governance.

## Step 3 - Understand The Minimal Operating Flow

ICFACTORY favors a controlled sequence:

1. observe the real state;
2. audit before changing;
3. identify authority and scope;
4. design the smallest safe change;
5. obtain explicit approval;
6. apply only the approved change;
7. validate behavior and evidence;
8. record the result.

This flow is explained in more detail in `the ICFACTORY method documentation`.

For onboarding, the important point is simple: ICFACTORY does not treat implementation as the first step. It treats understanding, authority and evidence as prerequisites for implementation.

## Step 4 - Open The Project Constitution Template

Open:

`governance/PROJECT_CONSTITUTION_TEMPLATE.md`

Use it as the starting artifact for adoption.

Do not copy the Constitutional Lexicon into the template. Do not reproduce the template inside another onboarding document. Work inside the template when you are ready to create a Project Constitution.

During the first pass, focus only on the major areas:

* project identification;
* constitutional compatibility;
* documentary governance;
* constitutional authorities;
* approval and vigencia;
* conformity and remediation;
* mission, objectives, priorities, restrictions and governance.

If a field cannot be completed yet, leave it as a controlled draft decision rather than inventing authority or evidence.

## Step 5 - Consult The Lexicon Only When Needed

Use:

`CONSTITUTIONAL_LEXICON.md`

The lexicon is the authoritative semantic reference. It is not the best first-read document.

Consult it when you need precision about terms such as validity, vigencia, constitutional approval, conformity, remediation or authority scope.

Do not use the lexicon as a replacement for the template. The lexicon defines meanings; the template structures a project constitution.

## Criteria For Initial Adoption Readiness

You are ready to continue adoption when you can answer:

* What is the project adopting ICFACTORY?
* What problem makes governance necessary?
* Which document is the Project Constitution draft?
* Which authorities must be identified?
* Which evidence is needed for validation, approval and vigencia?
* Which parts of the project are still unknown or not applicable?
* Which ICFACTORY documents are references, and which are working artifacts?

If these questions cannot be answered yet, continue reading and mapping before attempting implementation changes.

## Next Reading

After this guide, read:

`DOCUMENT_MAP.md`

Use it to decide which document to open next according to your goal.

If your goal is adoption, continue with the Project Constitution Template.

If your goal is semantic precision, use the Constitutional Lexicon.

If your goal is historical context, use History and Roadmap later, after the core onboarding path is understood.


## Incorporation Note

This document was adapted during GP-FW-04B for the autonomous icfactory-framework repository layout. The original source path was C:\HANDA_CORE\ICFACTORY\GETTING_STARTED.md. The source hash and adaptation are recorded in provenance/HANDA_CORE_INCORPORATION_MANIFEST.md.
