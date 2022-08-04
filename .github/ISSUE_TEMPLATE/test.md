___
name: test Issue
about: For any issues involving a League Loader
title: "[LEAGUE LOADER]"
labels: ''
assignees: joeyagreco

body:

- type: dropdown
  attributes:
  label: League Loader
  options:
  - ESPN
  - Sleeper
    validations:
    required: true

- type: textarea
  attributes:
  label: Summary
  description: Describe the issue briefly below.
  validations:
  required: true
- ___