# Stock Count Board

`index.html` is a single-page tool. Open it in a browser and paste an inventory report.

- Expected rows: `VENDOR <tab> ITEM# Name · Style · Category [codes] <tab> qty <tab> ---`
- ASH rows go to the **Ashley** tab, other vendors go to **Non-Ashley**, and rows in a Bedding or Mattress category go to **Bedding**.
- Each report is a snapshot for its category. A report with only ASH rows replaces only Ashley counts in that category. A mixed report replaces every vendor in that category. Items that drop off a new report stay listed with 0 (Out).
- Excel or CSV files with a header row also work. You pick the columns before anything is added.
- Data is saved in your browser's local storage, so it stays on that browser only.
