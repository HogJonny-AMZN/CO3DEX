# Pull Request Merge Summary

## Overview
This PR consolidates and applies the changes from all open Dependabot pull requests that were updating Ruby gem dependencies in the `Gemfile.lock` file.

## Pull Requests Consolidated

### PR #66: Bump backports from 3.25.1 to 3.25.2
- **Status**: Changes applied (via PR #72)
- **Change**: Updated `backports` gem from version 3.25.1 to 3.25.2
- **Purpose**: Minor version update with bug fixes

### PR #67: Bump tzinfo-data from 1.2025.1 to 1.2025.2
- **Status**: Changes applied (via PR #72)
- **Change**: Updated `tzinfo-data` gem from version 1.2025.1 to 1.2025.2
- **Purpose**: Timezone database update to version 2025b

### PR #70: Bump rake from 13.2.1 to 13.3.1
- **Status**: Previously applied (via PR #72 consolidation commit)
- **Change**: Updated `rake` gem from version 13.2.1 to 13.3.1 (also updated `jgd` from 1.13.1 to 1.14.0)
- **Purpose**: Minor version update with improvements

### PR #73: Bump tzinfo-data from 1.2025.2 to 1.2025.3
- **Status**: Changes applied
- **Change**: Updated `tzinfo-data` from 1.2025.2 to 1.2025.3; updated `concurrent-ruby` from 1.3.5 to 1.3.6
- **Purpose**: Timezone database update to version 2025c

### PR #74: Bump faraday-retry from 2.3.2 to 2.4.0
- **Status**: Changes applied
- **Changes**:
  - `faraday` 2.14.0 → 2.14.1
  - `faraday-net_http` 3.4.1 → 3.4.2
  - `faraday-retry` 2.3.2 → 2.4.0
  - `json` 2.15.0 → 2.18.1
  - `net-http` 0.6.0 → 0.9.1
  - `uri` 1.0.3 → 1.1.1
- **Purpose**: Minor version updates with improvements and security patches

### PR #75: Bump kramdown from 2.5.1 to 2.5.2
- **Status**: Changes applied
- **Change**: Updated `kramdown` from 2.5.1 to 2.5.2 (requires `rexml >= 3.4.4`)
- **Purpose**: Minor version update with bug fixes

### PR #76: Bump backports from 3.25.2 to 3.25.3
- **Status**: Changes applied
- **Change**: Updated `backports` from 3.25.2 to 3.25.3 (continuing from PR #66 which updated 3.25.1 → 3.25.2)
- **Purpose**: Minor version update with bug fixes

## Conflict Resolution

All PRs were attempting to update the same file (`Gemfile.lock`) but in different sections. Because all PRs were based on different older commits of the main branch, they could not be merged sequentially without rebasing.

Instead of rebasing each PR individually, all dependency updates were combined into a single commit in this PR. This approach:
1. ✅ Applies all dependency updates at once
2. ✅ Avoids sequential merge conflicts
3. ✅ Maintains a clean commit history
4. ✅ Ensures all dependencies are updated together

## Security Review

All updated dependencies were checked against the GitHub Advisory Database:
- ✅ No vulnerabilities found in backports 3.25.3
- ✅ No vulnerabilities found in rake 13.3.1
- ✅ No vulnerabilities found in tzinfo-data 1.2025.3
- ✅ No vulnerabilities found in faraday-retry 2.4.0
- ✅ No vulnerabilities found in kramdown 2.5.2
- ✅ No vulnerabilities found in concurrent-ruby 1.3.6
- ✅ No vulnerabilities found in json 2.18.1
- ✅ No vulnerabilities found in uri 1.1.1

## Next Steps

Once this PR is merged to main:
1. PRs #70, #73, #74, #75, and #76 can be closed as their changes are now incorporated
2. The repository will be up to date with the latest compatible versions of all dependencies
3. Future Dependabot PRs will be based on the updated `Gemfile.lock`
