import React, { useMemo } from 'react';
import Plot from 'react-plotly.js';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Info } from 'lucide-react';

/**
 * DynamicVisualization component that generates charts based on AI recommendations.
 * 
 * Renders visualizations dynamically based on the dataset structure analysis.
 */
const DynamicVisualization = ({ chartConfig, data, title, description }) => {
  const chartData = useMemo(() => {
    if (!chartConfig || !data) {
      console.log('DynamicVisualization: Missing chartConfig or data', { chartConfig, data });
      return null;
    }

    // Support both 'visualization' and 'chart_type' properties
    const vizType = chartConfig.visualization || chartConfig.chart_type;
    const variable = chartConfig.variable || (chartConfig.variables && chartConfig.variables[0]);
    const variables = chartConfig.variables || (variable ? [variable] : []);

    console.log('DynamicVisualization: Generating chart', {
      type: chartConfig.type,
      variable,
      variables,
      vizType,
      dataKeys: Object.keys(data),
      title,
      chartConfig
    });

    try {
      switch (vizType) {
        case 'pie':
          return generatePieChart(data, variable);

        case 'bar':
          return generateBarChart(data, variables);

        case 'scatter':
          return generateScatterChart(data, variables);

        case 'line':
          return generateLineChart(data, variables);

        case 'box':
          return generateBoxChart(data, variables);

        case 'heatmap':
          return generateHeatmap(data, variables);

        case 'histogram':
          return generateHistogram(data, variables);

        default:
          console.warn('DynamicVisualization: Unknown visualization type', vizType);
          return null;
      }
    } catch (error) {
      console.error('Error generating chart:', error, { chartConfig, data });
      return null;
    }
  }, [chartConfig, data, title]);

  if (!chartData) {
    return (
      <Card className="border-pink-200">
        <CardHeader>
          <CardTitle>{title || 'Visualización'}</CardTitle>
          {description && <CardDescription>{description}</CardDescription>}
        </CardHeader>
        <CardContent>
          <Alert className="border-blue-200 bg-blue-50">
            <Info className="h-4 w-4" />
            <AlertDescription>
              No se pudo generar la visualización para esta configuración.
            </AlertDescription>
          </Alert>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="border-pink-200">
      <CardHeader>
        <CardTitle>{title || chartConfig.title || 'Visualización'}</CardTitle>
        {(description || chartConfig.description) && (
          <CardDescription>{description || chartConfig.description}</CardDescription>
        )}
      </CardHeader>
      <CardContent>
        <Plot
          data={chartData.data}
          layout={chartData.layout}
          config={{ responsive: true, displayModeBar: false }}
          style={{ width: '100%', height: '400px' }}
        />
      </CardContent>
    </Card>
  );
};

// Helper functions to generate different chart types

const generatePieChart = (data, variable) => {
  console.log('generatePieChart:', { variable, dataKeys: Object.keys(data), hasVariable: !!data[variable] });

  if (!data[variable]) {
    console.warn('generatePieChart: Variable not found in data', { variable, availableKeys: Object.keys(data) });
    return null;
  }

  // Handle nested structure from dynamic summary (categorical_stats)
  let distribution = data[variable];
  if (distribution && typeof distribution === 'object' && distribution.distribution) {
    distribution = distribution.distribution;
  }

  const labels = Object.keys(distribution);
  const values = Object.values(distribution);

  console.log('generatePieChart: Generated chart data', { labels, values });

  return {
    data: [{
      type: 'pie',
      labels: labels,
      values: values,
      marker: {
        colors: ['#ec4899', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6']
      },
      textinfo: 'label+percent',
      hovertemplate: '<b>%{label}</b><br>Cantidad: %{value}<br>Porcentaje: %{percent}<extra></extra>'
    }],
    layout: {
      showlegend: true,
      legend: { orientation: 'h', y: -0.1 },
      margin: { t: 20, b: 60, l: 20, r: 20 }
    }
  };
};

const generateBarChart = (data, variables) => {
  const variable = variables[0];
  if (!data[variable]) return null;

  // Handle nested structure from dynamic summary (categorical_stats)
  let distribution = data[variable];
  if (distribution && typeof distribution === 'object' && distribution.distribution) {
    distribution = distribution.distribution;
  }

  const labels = Object.keys(distribution);
  const values = Object.values(distribution);

  return {
    data: [{
      type: 'bar',
      x: labels,
      y: values,
      marker: {
        color: '#ec4899',
        line: { color: '#be185d', width: 1 }
      },
      hovertemplate: '<b>%{x}</b><br>Cantidad: %{y}<extra></extra>'
    }],
    layout: {
      xaxis: { title: variable },
      yaxis: { title: 'Frecuencia' },
      margin: { t: 20, b: 60, l: 60, r: 20 }
    }
  };
};

const generateScatterChart = (data, variables) => {
  if (variables.length < 2) return null;

  const [xVar, yVar] = variables;

  // Check if we have raw data arrays
  if (Array.isArray(data[xVar]) && Array.isArray(data[yVar])) {
    return {
      data: [{
        type: 'scatter',
        mode: 'markers',
        x: data[xVar],
        y: data[yVar],
        marker: {
          color: '#3b82f6',
          size: 8,
          opacity: 0.6
        },
        hovertemplate: `<b>${xVar}</b>: %{x}<br><b>${yVar}</b>: %{y}<extra></extra>`
      }],
      layout: {
        xaxis: { title: xVar },
        yaxis: { title: yVar },
        margin: { t: 20, b: 60, l: 60, r: 20 }
      }
    };
  }

  // If we only have summary statistics, create a bar chart showing the statistics
  console.warn('generateScatterChart: Converting to bar chart due to summary data');

  // Collect statistics for each variable
  const stats = [];
  const statLabels = [];

  variables.forEach(variable => {
    if (data[variable]) {
      const varData = data[variable];
      if (varData.mean !== undefined) {
        stats.push({
          variable: variable,
          mean: varData.mean,
          median: varData.median,
          min: varData.min,
          max: varData.max
        });
      }
    }
  });

  if (stats.length === 0) return null;

  // Create a grouped bar chart showing statistics
  return {
    data: stats.map((stat, index) => ({
      type: 'bar',
      name: stat.variable,
      x: ['Mínimo', 'Media', 'Mediana', 'Máximo'],
      y: [stat.min, stat.mean, stat.median, stat.max],
      marker: {
        color: ['#3b82f6', '#10b981', '#f59e0b', '#ec4899'][index % 4]
      }
    })),
    layout: {
      barmode: 'group',
      xaxis: { title: 'Estadística' },
      yaxis: { title: 'Valor' },
      margin: { t: 20, b: 60, l: 60, r: 20 },
      showlegend: true,
      legend: { orientation: 'h', y: -0.2 }
    }
  };
};

const generateLineChart = (data, variables) => {
  const variable = variables[0];
  if (!data[variable]) return null;

  // Handle nested structure from dynamic summary (categorical_stats)
  let distribution = data[variable];
  if (distribution && typeof distribution === 'object' && distribution.distribution) {
    distribution = distribution.distribution;
  }

  const labels = Object.keys(distribution);
  const values = Object.values(distribution);

  return {
    data: [{
      type: 'scatter',
      mode: 'lines+markers',
      x: labels,
      y: values,
      line: { color: '#10b981', width: 2 },
      marker: { color: '#10b981', size: 6 },
      hovertemplate: '<b>%{x}</b><br>Valor: %{y}<extra></extra>'
    }],
    layout: {
      xaxis: { title: variable },
      yaxis: { title: 'Valor' },
      margin: { t: 20, b: 60, l: 60, r: 20 }
    }
  };
};

const generateBoxChart = (data, variables) => {
  const colors = ['#ec4899', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6'];

  const traces = variables.map((variable, index) => {
    if (!data[variable]) return null;

    const varData = data[variable];

    // Check if we have raw data array
    if (Array.isArray(varData)) {
      return {
        type: 'box',
        y: varData,
        name: variable,
        marker: { color: colors[index % colors.length] },
        boxmean: 'sd',
        hovertemplate: `<b>${variable}</b><br>Valor: %{y}<extra></extra>`
      };
    }

    // If we have summary statistics, create a box plot from statistics
    if (varData.min !== undefined && varData.max !== undefined) {
      // Create a synthetic box plot using the statistics
      return {
        type: 'box',
        name: variable,
        q1: [varData.q25 || varData.min],
        median: [varData.median || varData.mean],
        q3: [varData.q75 || varData.max],
        lowerfence: [varData.min],
        upperfence: [varData.max],
        mean: [varData.mean],
        marker: { color: colors[index % colors.length] },
        boxmean: true,
        hovertemplate: `<b>${variable}</b><br>` +
          `Min: ${varData.min.toFixed(2)}<br>` +
          `Q1: ${(varData.q25 || varData.min).toFixed(2)}<br>` +
          `Mediana: ${(varData.median || varData.mean).toFixed(2)}<br>` +
          `Q3: ${(varData.q75 || varData.max).toFixed(2)}<br>` +
          `Max: ${varData.max.toFixed(2)}<br>` +
          `Media: ${varData.mean.toFixed(2)}<extra></extra>`
      };
    }

    return null;
  }).filter(trace => trace !== null);

  if (traces.length === 0) return null;

  return {
    data: traces,
    layout: {
      yaxis: { title: 'Valor' },
      showlegend: true,
      margin: { t: 20, b: 60, l: 60, r: 20 }
    }
  };
};

const generateHeatmap = (data, variables) => {
  // Expecting data to be a correlation matrix
  if (!data.matrix || !data.labels) return null;

  return {
    data: [{
      type: 'heatmap',
      z: data.matrix,
      x: data.labels,
      y: data.labels,
      colorscale: [
        [0, '#3b82f6'],
        [0.5, '#ffffff'],
        [1, '#ec4899']
      ],
      zmid: 0,
      text: data.matrix.map(row =>
        row.map(val => val.toFixed(2))
      ),
      texttemplate: '%{text}',
      textfont: { size: 10 },
      hovertemplate: '<b>%{x}</b> vs <b>%{y}</b><br>Correlación: %{z:.3f}<extra></extra>'
    }],
    layout: {
      xaxis: { side: 'bottom' },
      yaxis: { autorange: 'reversed' },
      margin: { t: 20, b: 100, l: 100, r: 20 }
    }
  };
};

const generateHistogram = (data, variables) => {
  const variable = variables[0];
  if (!data[variable]) return null;

  const varData = data[variable];

  // Check if we have raw data array
  if (Array.isArray(varData)) {
    return {
      data: [{
        type: 'histogram',
        x: varData,
        marker: {
          color: '#3b82f6',
          line: { color: '#1e40af', width: 1 }
        },
        hovertemplate: '<b>Rango</b>: %{x}<br>Frecuencia: %{y}<extra></extra>'
      }],
      layout: {
        xaxis: { title: variable },
        yaxis: { title: 'Frecuencia' },
        margin: { t: 20, b: 60, l: 60, r: 20 }
      }
    };
  }

  // If we have summary statistics with distribution, use it
  if (varData.distribution) {
    const labels = Object.keys(varData.distribution);
    const values = Object.values(varData.distribution);

    return {
      data: [{
        type: 'bar',
        x: labels,
        y: values,
        marker: {
          color: '#3b82f6',
          line: { color: '#1e40af', width: 1 }
        },
        hovertemplate: '<b>%{x}</b><br>Frecuencia: %{y}<extra></extra>'
      }],
      layout: {
        xaxis: { title: variable },
        yaxis: { title: 'Frecuencia' },
        margin: { t: 20, b: 60, l: 60, r: 20 }
      }
    };
  }

  // If we only have statistics, create a simple representation
  if (varData.mean !== undefined) {
    return {
      data: [{
        type: 'bar',
        x: ['Mínimo', 'Q1', 'Mediana', 'Media', 'Q3', 'Máximo'],
        y: [
          varData.min,
          varData.q25 || varData.min,
          varData.median || varData.mean,
          varData.mean,
          varData.q75 || varData.max,
          varData.max
        ],
        marker: {
          color: '#3b82f6',
          line: { color: '#1e40af', width: 1 }
        },
        hovertemplate: '<b>%{x}</b><br>Valor: %{y:.2f}<extra></extra>'
      }],
      layout: {
        xaxis: { title: 'Estadística' },
        yaxis: { title: variable },
        margin: { t: 20, b: 60, l: 60, r: 20 }
      }
    };
  }

  return null;
};

export default DynamicVisualization;

