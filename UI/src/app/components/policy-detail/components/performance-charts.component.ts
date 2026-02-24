import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { BaseChartDirective } from 'ng2-charts';
import { Chart, ChartConfiguration, ChartType, registerables } from 'chart.js';

// Register Chart.js components
Chart.register(...registerables);

interface Alternative {
  productName: string;
  carrier: string;
  capRate: number;
  canSell?: boolean;
}

@Component({
  selector: 'app-performance-charts',
  standalone: true,
  imports: [CommonModule, MatIconModule, BaseChartDirective],
  templateUrl: './performance-charts.component.html',
  styleUrls: ['./performance-charts.component.scss']
})
export class PerformanceChartsComponent implements OnInit {
  @Input() currentPolicyName: string = '';
  @Input() currentCapRate: number = 0;
  @Input() currentAccountValue: number = 150000;
  @Input() alternatives: Alternative[] = [];
  @Input() incomeGoal: number = 70000;

  @ViewChild(BaseChartDirective) chart?: BaseChartDirective;

  // Account Value Projection Chart
  accountValueChartData: ChartConfiguration['data'] = {
    datasets: [],
    labels: []
  };

  accountValueChartOptions: ChartConfiguration['options'] = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'bottom',
        labels: {
          usePointStyle: true,
          padding: 15
        }
      },
      tooltip: {
        mode: 'index',
        intersect: false,
        callbacks: {
          label: (context) => {
            const label = context.dataset.label || '';
            const value = context.parsed.y;
            if (value === null || value === undefined) return label;
            return `${label}: $${(value / 1000).toFixed(0)}k`;
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: false,
        ticks: {
          callback: (value) => `$${(Number(value) / 1000).toFixed(0)}k`
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)'
        }
      },
      x: {
        grid: {
          display: false
        }
      }
    },
    interaction: {
      mode: 'index',
      intersect: false
    }
  };

  accountValueChartType: ChartType = 'line';

  // Interest Rate Projection Chart
  rateChartData: ChartConfiguration['data'] = {
    datasets: [],
    labels: []
  };

  rateChartOptions: ChartConfiguration['options'] = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'bottom',
        labels: {
          usePointStyle: true,
          padding: 15
        }
      },
      tooltip: {
        mode: 'index',
        intersect: false,
        callbacks: {
          label: (context) => {
            const label = context.dataset.label || '';
            const value = context.parsed.y;            if (value === null || value === undefined) return label;            return `${label}: ${value.toFixed(2)}%`;
          }
        }
      },
      filler: {
        propagate: false
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 8,
        ticks: {
          callback: (value) => `${value}%`
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)'
        }
      },
      x: {
        title: {
          display: true,
          text: 'Year'
        },
        grid: {
          display: false
        }
      }
    },
    interaction: {
      mode: 'index',
      intersect: false
    }
  };

  rateChartType: ChartType = 'line';

  ngOnInit(): void {
    this.generateAccountValueProjections();
    this.generateRateProjections();
  }

  private generateAccountValueProjections(): void {
    const years = 21; // 0 to 20
    const labels = Array.from({ length: years }, (_, i) => i.toString());

    const datasets = [];

    // Current Policy
    const currentData = this.projectAccountValue(
      this.currentAccountValue,
      this.currentCapRate,
      years
    );
    datasets.push({
      label: this.currentPolicyName || 'Current Policy',
      data: currentData,
      borderColor: '#5b9bd5',
      backgroundColor: 'rgba(91, 155, 213, 0.1)',
      borderWidth: 2,
      pointRadius: 0,
      pointHoverRadius: 5,
      tension: 0.4
    });

    // Alternatives
    const colors = ['#70ad47', '#ffc000', '#c55a11'];
    this.alternatives.slice(0, 3).forEach((alt, index) => {
      const altData = this.projectAccountValue(
        this.currentAccountValue,
        alt.capRate,
        years
      );
      
      const dataset: any = {
        label: `${alt.productName} - Value`,
        data: altData,
        borderColor: colors[index],
        backgroundColor: `${colors[index]}20`,
        borderWidth: 2,
        pointRadius: 0,
        pointHoverRadius: 5,
        tension: 0.4
      };

      // Add dashed border for products that cannot be sold
      if (alt.canSell === false) {
        dataset.borderDash = [5, 5];
      }

      datasets.push(dataset);
    });

    // Income Goal Line
    datasets.push({
      label: 'Income Goal',
      data: Array(years).fill(this.incomeGoal),
      borderColor: '#ed7d31',
      backgroundColor: 'transparent',
      borderWidth: 2,
      borderDash: [10, 5],
      pointRadius: 0,
      pointHoverRadius: 0,
      tension: 0
    });

    this.accountValueChartData = {
      labels,
      datasets
    };
  }

  private generateRateProjections(): void {
    const years = 11; // 0 to 10
    const labels = Array.from({ length: years }, (_, i) => i.toString());

    const datasets = [];

    // Get top 3 alternatives for rate projections
    const topAlternatives = this.alternatives.slice(0, 3);
    const altNames = topAlternatives.map(alt => {
      const shortName = alt.productName.includes('MYGA') 
        ? alt.productName.split(' ').slice(0, -1).join(' ')
        : alt.productName.split(' ').slice(0, 2).join(' ');
      return shortName;
    });

    const colors = ['#5b9bd5', '#70ad47', '#ffc000'];

    topAlternatives.forEach((alt, index) => {
      // Conservative scenario
      const conservativeData = this.projectRateScenario(alt.capRate, years, 'conservative');
      datasets.push({
        label: altNames[index],
        data: conservativeData,
        borderColor: colors[index],
        backgroundColor: 'transparent',
        borderWidth: 2,
        pointRadius: 0,
        pointHoverRadius: 5,
        tension: 0.4,
        fill: false
      });
    });

    // Add shaded area for the range
    if (topAlternatives.length > 0) {
      const firstAlt = topAlternatives[0];
      const conservativeData = this.projectRateScenario(firstAlt.capRate, years, 'conservative');
      
      datasets.push({
        label: '',
        data: conservativeData,
        borderColor: 'transparent',
        backgroundColor: 'rgba(200, 200, 180, 0.3)',
        borderWidth: 0,
        pointRadius: 0,
        fill: 'origin',
        tension: 0.4
      });
    }

    this.rateChartData = {
      labels,
      datasets
    };
  }

  private projectAccountValue(initialValue: number, annualRate: number, years: number): number[] {
    const values = [initialValue];
    let currentValue = initialValue;

    for (let i = 1; i < years; i++) {
      currentValue = currentValue * (1 + annualRate / 100);
      values.push(currentValue);
    }

    return values;
  }

  private projectRateScenario(baseRate: number, years: number, scenario: 'conservative' | 'expected' | 'optimistic'): number[] {
    const rates = [];
    const startRate = baseRate;
    
    // Different decline patterns based on scenario
    const declineRates = {
      conservative: 0.15,  // 15% decline per year
      expected: 0.12,      // 12% decline per year
      optimistic: 0.08     // 8% decline per year
    };

    const decline = declineRates[scenario];

    for (let i = 0; i < years; i++) {
      const rate = startRate * Math.pow(1 - decline, i);
      rates.push(Math.max(rate, 1.0)); // Floor at 1%
    }

    return rates;
  }
}
