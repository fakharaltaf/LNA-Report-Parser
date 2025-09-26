# Configuration

This directory contains all configuration files for the LNA Bot.

## Files

### `competency_classification.md`
Defines which competencies are classified as "niche" vs "common":
- **Niche**: Specialized skills requiring SDP training
- **Common**: Widely applicable skills that can use standard training methods

### `skills_mapping.md`
Maps each competency to its associated skills for detailed recommendations.

### `business_rules_config.md`
Documents the business rules and thresholds used for training type decisions.

## Customization

To customize the bot's behavior:

1. **Add new competencies**: Update `competency_classification.md`
2. **Modify skills**: Edit `skills_mapping.md`
3. **Change thresholds**: Modify the business rules in the source code

## File Format

All configuration files use Markdown format with specific structure:
- Section headers with `##`
- Competency names as subsection headers with `###`
- Skills listed with `-` bullets