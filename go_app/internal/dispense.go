package internal

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
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
