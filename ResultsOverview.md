# Does Internet Acess Increase Voter Turnout? Evidence from 15 African countries

## Research Question
Does higher internet access correlate with higher voter turnout in African countries?

## Data
- **15 African countries** (Botswana, Egypt, Ethiopia, Ghana, Kenya, Morocco, Mozambique, Nigeria, Rwanda, Senegal, South Africa, Tanzania, Tunisia, Uganda, Zimbabwe)
- **Internet access**: % of population using internet (year closest to election)
- **Voter turnout**: % of registered voters who voted (most recent national election)
- **GDP per capita**: 2023 (control variable, not used in final model)

## Method
- Linear regression (internet access → voter turnout)
- Data cleaning: filled missing internet values with nearest available year
- Visualization: scatter plots, regression line with 95% CI, bar charts

## Key Result
- **R² = 0.08** → Internet access explains only **8% of the variance** in voter turnout
- **P‑value = 0.31** (not statistically significant at p < 0.05)
- **Slope = −0.18** → weak negative relationship (more internet, slightly lower turnout, but not meaningful)

## Outliers: Morocco & Rwanda

| Country | Internet Access (%) | Voter Turnout (%) | Expected Turnout (from model) | Deviation |
|---------|--------------------|-------------------|-------------------------------|-----------|
| **Morocco** | 88.1% | 37.1% | ~55% | **−18%** (much lower than predicted) |
| **Rwanda** | 34.2% | 98.0% | ~45% | **+53%** (much higher than predicted) |

Both countries fall far from the regression line in opposite directions.

## Why Are They Outliers? (Hypotheses)

### Morocco (high internet, very low turnout)
- Parliamentary elections seen as less important than presidential ones
- Political distrust / apathy ("boycott culture")
- Internet used for information, not mobilization

### Rwanda (moderate internet, extremely high turnout)
- **Compulsory voting** (enforced by local authorities)
- Strong civic education campaigns
- Post‑genocide political culture of participation
- Possible social desirability bias in reported turnout

## Next Steps / Future Research
- Add **election type** (presidential vs parliamentary) as a control
- Test **compulsory voting** as a dummy variable
- Include **political trust** or **press freedom** indices
- Run **case studies** on Morocco and Rwanda separately
- Collect **turnout as % of voting‑age population** (not just registered voters)

## Files in This Folder
- `analysis_summary.md` – This file
- All figures: `scatter_internet_turnout.png`, `regression_analysis.png`, `bar_by_country.png`
- Merged data: `merged_internet_turnout.csv`
- Full code: `code.py` (in root)

## Author
Abdellah IK.
