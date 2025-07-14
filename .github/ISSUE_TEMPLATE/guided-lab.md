name: Guided Lab
description: Submit your guided lab for this module
title: "[Guided Lab] Week XX: <Topic>"
labels: ["guided-lab"]
body:
  - type: markdown
    attributes:
      value: |
        ## Guided Lab Submission

  - type: input
    id: week
    attributes:
      label: Week Number
      placeholder: e.g. 02
    validations:
      required: true

  - type: textarea
    id: link
    attributes:
      label: Link to your branch/PR
      description: Paste the link to your lab branch or PR.
    validations:
      required: true

  - type: textarea
    id: reflection
    attributes:
      label: Reflection
      description: Paste your completed `REFLECTION.md` here.
    validations:
      required: true
