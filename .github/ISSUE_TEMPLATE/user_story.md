---
name: "User Story"
description: "Create a user story with acceptance criteria"
title: "[Story] <concise title>"
labels: ["user-story"]
assignees: []
body:
  - type: textarea
    id: story
    attributes:
      label: Story
      description: As a <role>, I want <capability> so that <benefit>.
      placeholder: |
        As a user, I want to ... so that ...
    validations:
      required: true
  - type: textarea
    id: acceptance
    attributes:
      label: Acceptance Criteria
      description: Provide a checklist of acceptance criteria.
      value: |
        - [ ] Criterion 1
        - [ ] Criterion 2
        - [ ] Criterion 3
    validations:
      required: true
---
