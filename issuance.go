package main

import (
	"encoding/json"
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

func getIssuancesByAddress(address string) ([]IssuanceData, error) {
	endpoint := "https://xchain.io/api/issuances/" + address
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

	uniqueIssuances := make([]IssuanceData, 0)
	seenAssets := make(map[string]bool)

	for _, issuance := range issuanceResponse.Data {
		if _, seen := seenAssets[issuance.Asset]; !seen {
			uniqueIssuances = append(uniqueIssuances, issuance)
			seenAssets[issuance.Asset] = true
		}
	}

	return uniqueIssuances, nil
}
