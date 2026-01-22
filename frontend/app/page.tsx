import Link from "next/link"
import { ArrowRight, TrendingUp, BarChart3, GitCompare } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export default function Home() {
  const popularETFs = [
    { ticker: "VOO", name: "Vanguard S&P 500 ETF", category: "Large Cap" },
    { ticker: "QQQ", name: "Invesco QQQ Trust", category: "Technology" },
    { ticker: "VTI", name: "Vanguard Total Stock Market ETF", category: "Total Market" },
    { ticker: "SCHD", name: "Schwab US Dividend Equity ETF", category: "Dividend" },
  ]

  const features = [
    {
      icon: TrendingUp,
      title: "Long-Term Simulation",
      description: "Simulate 10-30 year investment scenarios with historical data",
    },
    {
      icon: BarChart3,
      title: "Portfolio Analysis",
      description: "Analyze CAGR, MDD, and total returns with detailed charts",
    },
    {
      icon: GitCompare,
      title: "Strategy Comparison",
      description: "Compare lump sum vs DCA and different portfolio allocations",
    },
  ]

  return (
    <div className="flex flex-col">
      {/* Hero Section */}
      <section className="container px-4 py-24 mx-auto">
        <div className="flex flex-col items-center text-center space-y-8">
          <h1 className="text-4xl md:text-6xl font-bold tracking-tight">
            ETF Investment Simulator
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl">
            Simulate long-term ETF investments with historical data.
            Learn the power of compound interest and dollar-cost averaging.
          </p>
          <div className="flex gap-4">
            <Link href="/simulate">
              <Button size="lg" className="gap-2">
                Start Simulation <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
            <Link href="/explore">
              <Button size="lg" variant="outline">
                Explore ETFs
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container px-4 py-16 mx-auto bg-muted/50">
        <div className="grid md:grid-cols-3 gap-8">
          {features.map((feature) => (
            <Card key={feature.title}>
              <CardHeader>
                <feature.icon className="h-10 w-10 text-primary mb-2" />
                <CardTitle>{feature.title}</CardTitle>
                <CardDescription>{feature.description}</CardDescription>
              </CardHeader>
            </Card>
          ))}
        </div>
      </section>

      {/* Popular ETFs Section */}
      <section className="container px-4 py-16 mx-auto">
        <div className="space-y-8">
          <div className="text-center space-y-2">
            <h2 className="text-3xl font-bold">Popular ETFs</h2>
            <p className="text-muted-foreground">
              Start with these popular ETFs for your simulation
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
            {popularETFs.map((etf) => (
              <Link key={etf.ticker} href={`/etf/${etf.ticker}`}>
                <Card className="hover:border-primary transition-colors cursor-pointer">
                  <CardHeader>
                    <CardTitle className="text-lg">{etf.ticker}</CardTitle>
                    <CardDescription className="text-sm">
                      {etf.name}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <span className="text-xs text-muted-foreground">
                      {etf.category}
                    </span>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}
