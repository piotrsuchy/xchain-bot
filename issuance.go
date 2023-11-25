package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

type IssuanceData struct {
	// Struct fields
	Asset     string `json:"asset"`
	FeePaid   string `json:"fee_paid"`
	Quantity  string `json:"quantity"`
	Timestamp uint64 `json:"timestamp"`
}

type IssuanceResponse struct {
	Data []IssuanceData `json:"data"`
}

func getUniqueAssetNames(issuances []IssuanceData) []string {
	uniqueAssets := make(map[string]struct{}) // A set to store unique asset names
	var assetNames []string

	for _, issuance := range issuances {
		if _, exists := uniqueAssets[issuance.Asset]; !exists {
			assetNames = append(assetNames, issuance.Asset)
			uniqueAssets[issuance.Asset] = struct{}{}
		}
	}

	return assetNames
}

func getIssuancesByAddress(address string) ([]IssuanceData, error) {
	var allIssuances []IssuanceData
	page := 1
	limit := 100

	for {
		endpoint := fmt.Sprintf("https://xchain.io/api/issuances/%s/%d/%d", address, page, limit)
		resp, err := http.Get(endpoint)
		if err != nil {
			return nil, err
		}
		defer resp.Body.Close()

		body, err := io.ReadAll(resp.Body)
		if err != nil {
			return nil, err
		}

		var issuanceResponse IssuanceResponse
		if err := json.Unmarshal(body, &issuanceResponse); err != nil {
			return nil, err
		}

		if len(issuanceResponse.Data) < limit {
			allIssuances = append(allIssuances, issuanceResponse.Data...)
			break
		}

		allIssuances = append(allIssuances, issuanceResponse.Data...)
		page++
	}

	return allIssuances, nil
}
