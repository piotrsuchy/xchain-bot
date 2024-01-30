package main

import (
	"fmt"
	"log"
	"os"
	"sort"
	"time"

	"github.com/piotrsuchy/xchain_bot/internal"
)

func main() {
	address := "1DRZVQe58Tr9WxDNYdJUbye3toH1zkedX" // Example address

	issuances, err := internal.GetIssuancesByAddress(address)
	if err != nil {
		log.Fatalf("Error fetching issuances: %v", err)
	}

	uniqueAssetNames := internal.GetUniqueAssetNames(issuances)
	fmt.Println("Unique Asset Names:", uniqueAssetNames)

	var allDispenses []internal.DispenseData
	for _, asset := range uniqueAssetNames {
		log.Printf("Fetching dispenses for asset %s", asset)
		dispenses, err := internal.GetDispensesByAsset(asset)
		if err != nil {
			log.Printf("Error fetching dispenses for asset %s: %v", asset, err)
			continue
		}
		allDispenses = append(allDispenses, dispenses...)
	}

	sort.Slice(allDispenses, func(i, j int) bool {
		return allDispenses[i].Timestamp > allDispenses[j].Timestamp
	})

	file, err := os.Create("dispenses.txt")
	if err != nil {
		log.Fatalf("Failed to create file: %v", err)
	}
	defer file.Close()

	for _, dispense := range allDispenses {
		timestamp := time.Unix(dispense.Timestamp, 0).UTC()
		_, err := fmt.Fprintf(file, "Asset: %s, Address: %s, Quantity: %s, Amount: %s, Date: %s\n",
			dispense.Asset, dispense.Address, dispense.Quantity, dispense.BtcAmount, timestamp.Format(time.RFC3339))
		if err != nil {
			log.Printf("Failed to write to file ")
		}
	}
}
