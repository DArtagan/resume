# William H. Weiskopf, IV

Cambridge, Massachusetts · United States of America

Phone: (+1) 720-663-9455 | Email: william@weiskopf.me | GitHub: github.com/dartagan | LinkedIn: linkedin.com/in/whweiskopf


# Skills

Flask · SQLAlchemy · PostgreSQL · Terraform · GitHub Actions · Docker · Nix · AWS EC2/S3/CloudFront · Auth0 · Aptible · Grafana · New Relic · Cursor · Python · Kubernetes & Kustomize · Jenkins Pipelines · Prefect · Node.js (Express & Vue) · Alembic · MS SQL Server · GraphQL · Pi agent harness · Claude Code · Claude API · Whisper · Local LLMs (Ollama) · FastAPI · OpenTofu/Terraform · Prometheus/Loki/Grafana · Flux CD · SOPS secrets · ZFS · TLS · Talos Linux · Proxmox · CoreDNS · Tailscale · OpenEBS

# Experience

## Ginkgo Bioworks: Biosecurity

**Staff Software Engineer**\
Boston, Massachusetts | March 2021 -- November 2025

Tech lead for a HIPAA-compliant pathogen surveillance platform --
COVID-19 in thousands of K-12 schools, with lab partners in 18 states,
then multipathogen surveillance at 11 international airports (126 origin
countries) -- processing 15M+ samples and underpinning \$733M in
revenue.

- Led a multi-year platform evolution from single-pathogen COVID testing
  to multipathogen biosurveillance -- refactoring live production
  systems while preserving historical data, existing visualizations, and
  CDC reporting pipelines.

- Redesigned the core data model, decomposing a monolithic record into a
  normalized three-tier relationship -- enabling multi-panel testing.

- Led a team of \~11 as interim team lead through a period of rapid
  organizational change -- running ceremonies, managing stakeholders,
  and keeping engineers focused on delivery; transitioned to a dedicated
  tech lead role once a manager was hired.

- Built the team's release process (code-freeze automation,
  release-engineer rotation), on-call, and a DR exercise; mentored
  junior engineers.

- DevOps: rebuilt CI/CD pipelines around Docker with GitHub Actions,
  codified infrastructure in Terraform (Auth0, AWS, Aptible, supporting
  services), migrated off legacy vendor systems, and achieved 8x build
  performance on self-hosted runners.

- Designed PHI removal from the platform as the business shifted from
  individual diagnostics to aggregate biosurveillance -- balancing
  regulatory compliance, data retention, and system simplification.

## Oliver Wyman: Digital

**Senior Software Engineer**\
Boston, Massachusetts | October 2017 -- February 2021

- DevOps: wrote idiomatic containers, stood up CI/CD into Kubernetes
  across Digital's project portfolio.

- Webservices: REST and GraphQL backends for analytics; built a system
  cataloguing all of Digital's projects and assets for InfoSec
  auditability.

- Data infrastructure: ETL and workflow tooling. Built out a schema
  migration framework for a major grocery retailer, eliminating
  downtime.

- Sustaining: led long-term operations for five projects in the mature
  phase of their lifecycle.

## Lockheed Martin: Space Systems

**Software Engineer -- Orion: NASA's next crewed spacecraft**\
Littleton, Colorado | September 2014 -- September 2017

- Principal architect in moving Orion ground software from pen and paper
  to full test automation, empowering NASA requirement verification.

- Built a Python/LaTeX-based engine for creating NASA deliverables,
  cutting months of paperwork for engineers (per deliverable) to a day.

- Subject-matter expert on the flight software verification automation
  tiger team, sharing processes proven on ground software.

# Education

**Colorado School of Mines** -- B.S. Engineering, Mechanical Emphasis
--- CS & Economics minors | December 2013

Capstone: NASA Lunabotics Competition: built a regolith mining robot and
competed with international teams at the Kennedy Space Center.

# Projects

## reelbarrow & AI-Assisted Engineering

2025 -- Present

- Designed a review workflow for agentic development: a spec per
  project, a pull request reviewed thread by thread, and offline checks
  every change must pass. 4 pull requests merged upstream (3 to
  nixpkgs).

- Diagnosed passthrough of a Blu-ray drive across three virtualization
  layers (Proxmox hypervisor, Talos VM, Kubernetes device plugin & pod),
  then specified a phased ripping pipeline and verified its CD, DVD and
  Blu-ray edge cases, with an agent implementing each phase.

- Building a service that files ripped discs into a video library, using
  an LLM (Claude) to match Whisper transcripts to episodes. Each
  automatic filing needs a second, independent signal, because the model
  can be consistently and confidently wrong.

## Private Infrastructure Cloud

2015 -- Present

- Architected a GitOps-driven platform from bare metal through immutable
  Kubernetes, hosting 24+ services, with archive-class file integrity.

- Redesigned backups after an audit found four silent failures (offsite
  replication had failed for seven months): a phased 3-2-1-0 spec,
  append-only restic, pull-only replication, per-dataset freshness
  checks. Pruned 30,404 snapshots to 1,083, reclaiming 2.32 TiB.
