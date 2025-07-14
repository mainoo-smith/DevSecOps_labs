name: ✅ Feedback
description: Provide feedback on someone’s lab submission
title: "[Feedback] Week XX: <Topic>"
labels: ["feedback"]
body:
  - type: input
    id: week
    attributes:
      label: Week Number
    validations:
      required: true

  - type: textarea
    id: feedback
    attributes:
      label: Feedback
      description: What was done well? What could be improved? Any security considerations?
