# William H. Weiskopf, IV

Cambridge, Massachusetts, 02139 · United States of America

Phone: (+1) 720-663-9455 | Email: william@weiskopf.me | GitHub: github.com/dartagan | LinkedIn: linkedin.com/in/whweiskopf


# Skills

Flask · SQLAlchemy · PostgreSQL · Terraform · GitHub Actions · Docker · Nix · AWS EC2/S3/CloudFront · Auth0 · Aptible · Grafana · New Relic · Heap · Python · Kubernetes & Kustomize · Jenkins Pipelines · Prefect · Node.js (Express & Vue) · Alembic · MS SQL Server · GraphQL · Python packaging · Pytest · LaTeX · Sphinx · Linux · Vim · Perforce · JIRA · Jenkins · Agile · Test-driven development · Elastic stack · Proxmox · Kubernetes · ZFS · Ansible · Samba · Mumble · Plex · Borg backup · Beets · NGINX

# Experience

## Ginkgo Bioworks: Biosecurity

**Staff Software Engineer**\
Boston, Massachusetts | March 2021 -- November 2025

Tech lead for a HIPAA-compliant pathogen surveillance platform --
initially for COVID-19 in thousands of K-12 classrooms & lab partners
across 18 states, then multipathogen biosurveillance across 11
international airports (126 origin countries). 15M+ samples processed,
\$733M revenue.

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
  codified infrastructure in Terraform (Auth0, AWS, Aptible, supporting
  services), migrated off legacy vendor systems, and achieved 8x build
  performance on self-hosted runners.

- Designed PHI removal from the platform as the business shifted from
  individual diagnostics to aggregate biosurveillance -- balancing
  regulatory compliance, data retention, and system simplification.

## Oliver Wyman: Digital

**Senior Software Engineer**\
Boston, Massachusetts | October 2017 -- February 2021

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

## Lockheed Martin: Space Systems

**Software Engineer -- Orion: NASA's next manned spacecraft**\
Littleton, Colorado | September 2014 -- September 2017

- Principal architect in moving Orion ground software from pen and paper
  to full test automation, empowering NASA requirement verification.

- Built a Python/LaTeX-based engine for creating NASA deliverables,
  cutting months of paperwork for engineers (per deliverable) to a day.

- Served as a subject matter expert on the flight software verification
  automation tiger team, sharing processes established while automating
  ground.

**Air Sciences, Inc.** -- Network Administrator (intern & part-time) |
November 2011 -- March 2014

**CSM Alumni Association** -- Software Developer -- Website, newsletter,
graphics, audio, video | August 2010 -- April 2014

# Education

**Colorado School of Mines (CSM)** -- B.S. Engineering, Mechanical
Emphasis --- Computer Science and Economics minors | December 2013
Capstone: NASA Lunabotics Competition: built a regolith mining robot and
competed with international teams at the Kennedy Space Center.

# Projects

## Extensive Homelab

2015 -- Present

Homelab for experimenting with containers, virtualization, and services
-- with archive-class robust file-integrity protections.
