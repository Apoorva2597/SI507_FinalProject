
# SI507 Final Project: Pharmacy Proximity Network

This project explores geographic accessibility of pharmacies in Michigan using network analysis. Pharmacies are modeled as nodes, and edges represent proximity within 2 miles using geodesic distance.

##  Dataset
- Source: [Kaggle Pharmacy Dataset](https://www.kaggle.com/datasets)
- Filtered to only include pharmacies in Michigan (2,259 total)
- A sample of 200 pharmacies was used for the network graph

##  Method
- Built using `NetworkX`, `geopy`, `pandas`, and `matplotlib`
- Constructed a graph where pharmacies are connected if they are within 2 miles of each other
- Visualized using both geographic and spring layouts

## Features / CLI Interactions
- View nearby pharmacies (within 2 miles)
- Find the shortest path between two pharmacies
- Identify the most connected pharmacy
- Get pharmacy info and a Google Maps link
- Search pharmacies by ZIP code

## Visualizations
Two types of layouts are included:
- **Map Layout**: Based on latitude/longitude (accurate locations)
- **Spring Layout**: Shows network structure clearly (visible edges)

## Files Included
- `SI507_FinalProject.py`: Python script with CLI + network logic
- `SI507_FinalProject_Report.pdf`: Final write-up
- `images/`: Visual outputs of the network
- `Pharmacies.csv`: Cleaned dataset sample 

## To Run
```bash
python SI507_FinalProject.py
```

---

Developed as part of the final project for SI507: Intermediate Programming, University of Michigan School of Information.
