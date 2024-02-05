package internal

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"strconv"
	"time"
)

type DispenseData struct {
	Address    string `json:"address"`
	Asset      string `json:"asset"`
	BlockIndex int    `json:"block_index"`
	BtcAmount  string `json:"btc_amount"`
	Dispenser  string `json:"dispenser"`
	Quantity   string `json:"quantity"`
	Timestamp  int64  `json:"timestamp"`
	TxHash     string `json:"tx_hash"`
}

type DispenseResponse struct {
	Data []DispenseData `json:"data"`
}

type RateLimitError struct {
	RetryAfter time.Duration
}

func (e *RateLimitError) Error() string {
	return fmt.Sprintf("rate limited; retry after %v", e.RetryAfter)
}

func GetDispensesByAssetWithRetry(asset string, maxRetries int) ([]DispenseData, error) {
	var allDispenses []DispenseData
	retries := 0
	delay := 1 * time.Second // Start with a 1-second delay

	for retries < maxRetries {
		dispenses, err := GetDispensesByAsset(asset)
		if err != nil {
			if _, ok := err.(*RateLimitError); ok {
				log.Printf("Rate limited. Retrying in %v...", delay)
				time.Sleep(delay)
				delay *= 2 // Double the delay for the next retry
				retries++
				continue
			} else {
				// Handle other types of errors
				return nil, err
			}
		}
		allDispenses = append(allDispenses, dispenses...)
		break // Success, exit loop
	}

	if retries == maxRetries {
		return nil, fmt.Errorf("max retries reached for asset %s", asset)
	}

	return allDispenses, nil
}

func GetDispensesByAsset(asset string) ([]DispenseData, error) {
	var allDispenses []DispenseData
	page := 1
	limit := 100

	for {
		endpoint := fmt.Sprintf("https://xchain.io/api/dispenses/%s/%d/%d", asset, page, limit)
		resp, err := http.Get(endpoint)
		if err != nil {
			return nil, err
		}
		defer resp.Body.Close()

		if resp.StatusCode == http.StatusTooManyRequests {
			retryAfterHeader := resp.Header.Get("Retry-After")
			retryAfter, err := strconv.Atoi(retryAfterHeader)
			if err != nil {
				// Default to 60 seconds if parsing fails
				retryAfter = 60
			}
			return nil, &RateLimitError{RetryAfter: time.Duration(retryAfter) * time.Second}
		}

		body, err := io.ReadAll(resp.Body)
		if err != nil {
			return nil, err
		}

		var dispenseResponse DispenseResponse
		err = json.Unmarshal(body, &dispenseResponse)
		if err != nil {
			return nil, err
		}

		if len(dispenseResponse.Data) < limit {
			allDispenses = append(allDispenses, dispenseResponse.Data...)
			break
		}

		allDispenses = append(allDispenses, dispenseResponse.Data...)
		page++
	}

	return allDispenses, nil
}
