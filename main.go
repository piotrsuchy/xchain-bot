package main

import (
	"fmt"
	"log"
)

func main() {
	address := "1DRZVQe58Tr9WxDNYdJUbye3toH1zkedX"

	issuances, err := getIssuancesByAddress(address)
	if err != nil {
		log.Fatalf("Error fetching issunaces: %v", err)
	}

	for _, issuance := range issuances {
		fmt.Printf("Asset: %s, Fee Paid: %s, Quantity: %s, Timestamp: %d\n",
			issuance.Asset, issuance.FeePaid, issuance.Quantity, issuance.Timestamp)
	}
}
