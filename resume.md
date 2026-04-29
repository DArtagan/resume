# William H. Weiskopf, IV

91 Westland Avenue · Boston, Massachusetts, 02115 · United States of America

Phone: (+1) 720-663-9455 | Email: william@weiskopf.me | GitHub: github.com/dartagan | LinkedIn: linkedin.com/in/whweiskopf

> "If you want to build a ship, don't herd people together to collect wood and don't assign them tasks and work, but rather teach them to long for the endless immensity of the sea." -Antoine de Saint-Exupery


# Experience

## Ginkgo Bioworks: Biosecurity

**Senior Software Engineer → Staff Software Engineer** \| Boston,
Massachusetts \| March 2021 -- November 2025

Tech lead for the software team behind a HIPAA-compliant pathogen
surveillance platform -- initially for COVID-19 in K-12 classrooms, then
multipathogen biosurveillance across 11 international airports. 15M+
samples processed, \$150M+ revenue.

- Led a multi-year platform evolution from single-pathogen COVID testing
  to multipathogen biosurveillance -- refactoring live production
  systems while preserving historical data, existing visualizations, and
  CDC reporting pipelines.

- Designed the Results & Sample Refactor: decomposed a monolithic data
  entity into three domain objects (sample, procedure, result) with
  one-to-many relationships -- enabling multi-panel testing without
  combinatorial data duplication.

- Grew from senior IC to de facto team lead for a team of \~11 --
  running ceremonies, managing stakeholders, and shielding the team from
  organizational churn. Transitioned to a traditional tech lead role
  when a dedicated manager was hired.

- DevOps: rebuilt CI/CD pipelines around Docker with GitHub Actions,
  codified infrastructure in Terraform (Auth0, AWS, supporting
  services), migrated off legacy vendor systems, and achieved 8x build
  performance on self-hosted runners.

- Designed PHI removal from the platform as the business shifted from
  individual diagnostics to aggregate biosurveillance -- balancing
  regulatory compliance, data retention, and system simplification.

*Skills: Python (Flask, SQLAlchemy, Alembic) · PostgreSQL · React &
TypeScript · Terraform · GitHub Actions · Docker · AWS (EC2, S3,
CloudFront) · Auth0 · Aptible (HIPAA) · Grafana · Heap*

## Oliver Wyman: Digital

**Senior Software Engineer** \| Boston, Massachusetts \| October 2017 --
February 2021

Oliver Wyman is a consulting company, where I had the opportunity to
work across a broad range of projects and roles. Some highlights below:

- DevOps: wrote idiomatic containers, stood up many projects with CI/CD
  into Kubernetes. Member of Special Interest Group to spread best
  practices. Synthesized an analytics stack to give consulting teams a
  platform for development, workflow scheduling, data operations, and
  execution.

- Webservices: primarily backends for analytics and database operations,
  interfaced with as REST and GraphQL API services. Developed a system
  that continuously collects & collates data on all of Digital
  projects/assets -- providing InfoSec auditability, surfacing lost
  items, and decreasing seek time for the Sustaining organization.

- Data infrastructure: built tooling for consultants to use in ETL,
  workflow automation, schema management, and computational scaling.
  Built out a migration-based schema framework for a project with a
  major grocery retailer, eliminating database down-time.

- Sustaining: lead long-term operations for five projects in the mature
  phase of their lifecycle.

*Skills: Python · Kubernetes & Kustomize · Jenkins Pipelines · Prefect ·
Node.js (Express & Vue) · Flask · Alembic · MS SQL Server · PostgreSQL ·
GraphQL*

## Lockheed Martin: Space Systems

**Software Engineer -- Orion: NASA's next manned spacecraft** \|
Littleton, Colorado \| September 2014 -- September 2017

- Principle architect in moving Orion ground software from pen and paper
  to full test automation, empowering NASA requirement verification.

- Built a Python/LaTeX-based engine for creating NASA deliverables,
  cutting months of paperwork for engineers (per deliverable) to a day.

- Served as a subject matter expert for the flight software verification
  automation tiger team, sharing processes established while automating
  ground.

- Built a recursive-descent compiler for a templating language similar
  to Jinja2.

- Voltunteer for Code Quest, Lockheed Martin's computer programming
  competition for high school teams.

*Skills: Python packaging · Pytest · LaTeX · Sphinx · Linux · Vim ·
Perforce · JIRA · Jenkins · Agile · Test-driven development · Elastic
stack*

**Air Sciences, Inc.** -- Network Administrator (intern & part-time) \|
November 2011 -- March 2014

**CSM Alumni Association** -- Software Developer -- Website, newsletter,
graphics, audio, video \| August 2010 -- April 2014

# Education

## Colorado School of Mines (CSM)

**B.S. in Engineering, Mechanical Emphasis --- Computer Science and
Economics minors** \| Golden, Colorado \| December 2013

- NASA Lunabotics Competition: built a full-size regolith collecting
  robot and competed with international teams at the Kennedy Space
  Center.

- FIRST Robotics Competitions: Mentored high school students in
  engineering princples. Refereed Colorado regional competitions (FRC
  and FLL).

*Skills: SolidWorks (FEA) · C++ · Java · Python · Machine shop ·
Feedback controls · Git · Arduino · MATLAB · LabVIEW*

# Projects

## [SingToWho.site](https://singtowho.site)

**June 2020**

A COVID-19 inpired hack to keep people safe and engaged during the
pandemic. When washing your hands, who should you sing happy birthday
to?

*Skills: HTML, Javascript, CSS · Google Cloud Storage · Cloudflare DNS ·
Skeleton CSS*

## Containerized Server

**2015 -- Present**

Homelab for experimenting with containers, virtualization, and services
-- with archive-class robust file-integrity protections.

*Skills: Docker (RancherOS) · ZFS · Traefik · RAID · btrfs · Samba ·
Mumble · Plex · Borg backup · Beets · NGINX*
