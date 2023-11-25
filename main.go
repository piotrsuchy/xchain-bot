package main

import (
	"fmt"
	"log"
)

func main() {
	address := "1DRZVQe58Tr9WxDNYdJUbye3toH1zkedX" // Example address

	issuances, err := getIssuancesByAddress(address)
	if err != nil {
		log.Fatalf("Error fetching issuances: %v", err)
	}

	uniqueAssetNames := getUniqueAssetNames(issuances)
	fmt.Println("Unique Asset Names:", uniqueAssetNames)
}
