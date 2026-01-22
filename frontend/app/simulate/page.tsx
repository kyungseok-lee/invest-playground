"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"

export default function SimulatePage() {
  const [ticker, setTicker] = useState("VOO")
  const [investmentType, setInvestmentType] = useState<"lump_sum" | "dca">("dca")
  const [initialAmount, setInitialAmount] = useState("10000")
  const [monthlyContribution, setMonthlyContribution] = useState("500")

  return (
    <div className="container px-4 py-8 mx-auto">
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="space-y-2">
          <h1 className="text-4xl font-bold">Investment Simulation</h1>
          <p className="text-muted-foreground">
            Configure your portfolio and see how it would have performed
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Portfolio Configuration</CardTitle>
              <CardDescription>
                Set up your investment parameters
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">ETF Ticker</label>
                <Input
                  value={ticker}
                  onChange={(e) => setTicker(e.target.value)}
                  placeholder="VOO"
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Investment Type</label>
                <div className="flex gap-2">
                  <Button
                    variant={investmentType === "lump_sum" ? "default" : "outline"}
                    onClick={() => setInvestmentType("lump_sum")}
                    className="flex-1"
                  >
                    Lump Sum
                  </Button>
                  <Button
                    variant={investmentType === "dca" ? "default" : "outline"}
                    onClick={() => setInvestmentType("dca")}
                    className="flex-1"
                  >
                    DCA
                  </Button>
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">
                  Initial Amount ($)
                </label>
                <Input
                  type="number"
                  value={initialAmount}
                  onChange={(e) => setInitialAmount(e.target.value)}
                />
              </div>

              {investmentType === "dca" && (
                <div className="space-y-2">
                  <label className="text-sm font-medium">
                    Monthly Contribution ($)
                  </label>
                  <Input
                    type="number"
                    value={monthlyContribution}
                    onChange={(e) => setMonthlyContribution(e.target.value)}
                  />
                </div>
              )}

              <Button className="w-full">Run Simulation</Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Simulation Results</CardTitle>
              <CardDescription>
                Your investment performance
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-12 text-muted-foreground">
                Configure your portfolio and run a simulation to see results
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
