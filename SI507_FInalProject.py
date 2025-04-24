import pandas as pd
import networkx as nx
from geopy.distance import geodesic
import matplotlib.pyplot as plt

# ----------------------------
# Load and prepare data
# ----------------------------
file_path = "C:/Users/Santosh/Downloads/archive (1)/Pharmacies.csv"
df = pd.read_csv(file_path, dtype=str, low_memory=False)

df = df[df["STATE"] == "MI"].copy()
df = df.rename(columns={"X": "Longitude", "Y": "Latitude"})
df = df.dropna(subset=["Longitude", "Latitude"])
df["Latitude"] = df["Latitude"].astype(float)
df["Longitude"] = df["Longitude"].astype(float)

print(f"✅ Loaded {len(df)} pharmacies in Michigan.")

# ----------------------------
# Build sample graph from 200 pharmacies
# ----------------------------
sample_df = df.head(200)
G = nx.Graph()

for idx, row in sample_df.iterrows():
    G.add_node(
        idx,
        name=row["NAME"],
        city=row["CITY"],
        lat=row["Latitude"],
        lon=row["Longitude"],
    )


def is_within_2_miles(coord1, coord2):
    return geodesic(coord1, coord2).miles <= 2


for i, row1 in sample_df.iterrows():
    for j, row2 in sample_df.iterrows():
        if i < j:
            coord1 = (row1["Latitude"], row1["Longitude"])
            coord2 = (row2["Latitude"], row2["Longitude"])
            if is_within_2_miles(coord1, coord2):
                G.add_edge(i, j)

print(
    f"📊 Sample network created with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges."
)

# ----------------------------
# Draw network with thick, visible edges
# ----------------------------

plt.figure(figsize=(12, 8))

# OPTION 1: True geographic layout
geo_pos = {node: (data["lon"], data["lat"]) for node, data in G.nodes(data=True)}
nx.draw_networkx_edges(G, geo_pos, alpha=0.4, edge_color="gray", width=2)
nx.draw_networkx_nodes(G, geo_pos, node_size=60, node_color="blue")
plt.title("Map Layout – Might Hide Edges")
plt.axis("off")
plt.tight_layout()
plt.show()

# OPTION 2: Force spring layout for visual clarity
plt.figure(figsize=(12, 8))
spring_pos = nx.spring_layout(G, seed=42)  # consistent layout
nx.draw_networkx_edges(G, spring_pos, alpha=0.5, edge_color="green", width=2)
nx.draw_networkx_nodes(G, spring_pos, node_size=60, node_color="orange")
plt.title("Spring Layout – Edges Should Be Visible")
plt.axis("off")
plt.tight_layout()
plt.show()


# ----------------------------
# User Interaction Functions
# ----------------------------
def get_neighbors(pharmacy_index):
    neighbors = list(G.neighbors(pharmacy_index))
    if not neighbors:
        print("No nearby pharmacies found.")
    else:
        print(f"{len(neighbors)} nearby pharmacies:")
        for neighbor in neighbors:
            print(f"- {G.nodes[neighbor]['name']} in {G.nodes[neighbor]['city']}")


def find_shortest_path(index1, index2):
    try:
        path = nx.shortest_path(G, source=index1, target=index2)
        print("→ Shortest path:")
        for idx in path:
            print(f"  - {G.nodes[idx]['name']} ({G.nodes[idx]['city']})")
    except nx.NetworkXNoPath:
        print("⚠️ No path found between the selected pharmacies.")


def get_most_connected():
    if G.number_of_edges() == 0:
        print("No connections found in the network.")
        return
    most_connected = max(G.degree, key=lambda x: x[1])
    node = G.nodes[most_connected[0]]
    print(
        f"⭐ Most connected pharmacy: {node['name']} in {node['city']} ({most_connected[1]} connections)"
    )


def get_info(idx):
    node = G.nodes[idx]
    print("📌 Pharmacy Info:")
    print("Name:", node["name"])
    print("City:", node["city"])
    print("Coordinates:", node["lat"], node["lon"])
    print(
        "Google Maps Link:",
        f"https://www.google.com/maps/search/?api=1&query={node['lat']},{node['lon']}",
    )


def search_by_zip(zip_code):
    matches = df[df["ZIP"].str.startswith(zip_code)]
    if matches.empty:
        print("❌ No pharmacies found in that ZIP code.")
    else:
        print(f"🔍 Pharmacies in ZIP code {zip_code}:")
        for _, row in matches.iterrows():
            print(f"- {row['NAME']} ({row['CITY']})")


# ----------------------------
# Show reference index for CLI
# ----------------------------
print("\n📍 Pharmacy Index Reference (Sample of 200)")
print("Index  |  Name                             |  City")
print("---------------------------------------------------------")
for idx in sample_df.index:
    name = G.nodes[idx]["name"][:30]
    city = G.nodes[idx]["city"]
    print(f"{idx:<6} | {name:<30} | {city}")

# ----------------------------
# Command-line Interaction Loop
# ----------------------------
while True:
    print("\n🔎 What would you like to do?")
    print("1. Find nearby pharmacies (neighbors)")
    print("2. Find shortest path between two pharmacies")
    print("3. Find the most connected pharmacy")
    print("4. Get info and Google Maps link for a pharmacy")
    print("5. Search pharmacies by ZIP code")
    print("6. Exit")

    choice = input("Enter choice (1–6): ")

    if choice == "1":
        idx = int(input("Enter pharmacy index (0–199): "))
        get_neighbors(idx)

    elif choice == "2":
        idx1 = int(input("Enter start pharmacy index (0–199): "))
        idx2 = int(input("Enter end pharmacy index (0–199): "))
        find_shortest_path(idx1, idx2)

    elif choice == "3":
        get_most_connected()

    elif choice == "4":
        idx = int(input("Enter pharmacy index (0–199): "))
        get_info(idx)

    elif choice == "5":
        zip_code = input("Enter 5-digit ZIP code: ")
        search_by_zip(zip_code)

    elif choice == "6":
        print("👋 Goodbye!")
        break

    else:
        print("❌ Invalid input. Please enter a number 1–6.")
