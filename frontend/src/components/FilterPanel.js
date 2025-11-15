import React, { useState, useEffect, useMemo } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Slider } from '@/components/ui/slider';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Filter, X, RefreshCw } from 'lucide-react';

/**
 * FilterPanel component for interactive data filtering.
 *
 * Allows filtering by:
 * - Age range
 * - Diagnosis
 * - Menopause status
 * - BIRADS classification
 * - Other clinical variables
 *
 * Args:
 *     onFilterChange (function): Callback when filters change
 *     summary (object): Data summary for filter options
 */
const FilterPanel = ({ onFilterChange, summary }) => {
  const [filters, setFilters] = useState({
    ageMin: 18,
    ageMax: 100,
    diagnosis: 'all',
    menopause: 'all',
    birads: 'all',
    breastfeeding: 'all'
  });

  // Reason: Compute active filters using useMemo to avoid unnecessary recalculations
  const activeFilters = useMemo(() => {
    const active = [];
    if (filters.ageMin > 18 || filters.ageMax < 100) {
      active.push({ key: 'age', label: `Edad: ${filters.ageMin}-${filters.ageMax}` });
    }
    if (filters.diagnosis !== 'all') {
      active.push({ key: 'diagnosis', label: `Diagnóstico: ${filters.diagnosis}` });
    }
    if (filters.menopause !== 'all') {
      active.push({ key: 'menopause', label: `Menopausia: ${filters.menopause}` });
    }
    if (filters.birads !== 'all') {
      active.push({ key: 'birads', label: `BIRADS: ${filters.birads}` });
    }
    if (filters.breastfeeding !== 'all') {
      active.push({ key: 'breastfeeding', label: `Lactancia: ${filters.breastfeeding}` });
    }
    return active;
  }, [filters]);

  // Reason: Notify parent component when filters change
  useEffect(() => {
    onFilterChange(filters);
  }, [filters, onFilterChange]);

  const handleAgeChange = (values) => {
    setFilters(prev => ({
      ...prev,
      ageMin: values[0],
      ageMax: values[1]
    }));
  };

  const handleSelectChange = (field, value) => {
    setFilters(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const removeFilter = (key) => {
    const resetValues = {
      age: { ageMin: 18, ageMax: 100 },
      diagnosis: { diagnosis: 'all' },
      menopause: { menopause: 'all' },
      birads: { birads: 'all' },
      breastfeeding: { breastfeeding: 'all' }
    };
    setFilters(prev => ({ ...prev, ...resetValues[key] }));
  };

  const resetAllFilters = () => {
    setFilters({
      ageMin: 18,
      ageMax: 100,
      diagnosis: 'all',
      menopause: 'all',
      birads: 'all',
      breastfeeding: 'all'
    });
  };

  return (
    <Card className="border-pink-200 shadow-md">
      <CardHeader className="bg-gradient-to-r from-pink-50 to-blue-50">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Filter className="w-5 h-5 text-pink-600" />
            <CardTitle className="text-lg">Filtros Interactivos</CardTitle>
          </div>
          {activeFilters.length > 0 && (
            <Button
              variant="ghost"
              size="sm"
              onClick={resetAllFilters}
              className="text-pink-600 hover:text-pink-700 hover:bg-pink-100"
            >
              <RefreshCw className="w-4 h-4 mr-1" />
              Limpiar
            </Button>
          )}
        </div>
        <CardDescription>
          Filtre los datos por variables clínicas
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6 pt-6">
        {/* Active Filters */}
        {activeFilters.length > 0 && (
          <div className="flex flex-wrap gap-2 pb-4 border-b border-pink-100">
            {activeFilters.map((filter) => (
              <Badge
                key={filter.key}
                variant="secondary"
                className="bg-pink-100 text-pink-800 hover:bg-pink-200 cursor-pointer"
                onClick={() => removeFilter(filter.key)}
              >
                {filter.label}
                <X className="w-3 h-3 ml-1" />
              </Badge>
            ))}
          </div>
        )}

        {/* Age Range Filter */}
        <div className="space-y-3">
          <Label className="text-sm font-semibold text-gray-700">
            Rango de Edad: {filters.ageMin} - {filters.ageMax} años
          </Label>
          <Slider
            min={18}
            max={100}
            step={1}
            value={[filters.ageMin, filters.ageMax]}
            onValueChange={handleAgeChange}
            className="w-full"
          />
          <div className="flex justify-between text-xs text-gray-500">
            <span>18 años</span>
            <span>100 años</span>
          </div>
        </div>

        {/* Diagnosis Filter */}
        <div className="space-y-2">
          <Label htmlFor="diagnosis" className="text-sm font-semibold text-gray-700">
            Diagnóstico
          </Label>
          <Select value={filters.diagnosis} onValueChange={(val) => handleSelectChange('diagnosis', val)}>
            <SelectTrigger id="diagnosis" className="border-pink-200 focus:ring-pink-500">
              <SelectValue placeholder="Seleccione diagnóstico" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Todos</SelectItem>
              <SelectItem value="Benigno">Benigno</SelectItem>
              <SelectItem value="Maligno">Maligno</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Menopause Filter */}
        <div className="space-y-2">
          <Label htmlFor="menopause" className="text-sm font-semibold text-gray-700">
            Estado de Menopausia
          </Label>
          <Select value={filters.menopause} onValueChange={(val) => handleSelectChange('menopause', val)}>
            <SelectTrigger id="menopause" className="border-pink-200 focus:ring-pink-500">
              <SelectValue placeholder="Seleccione estado" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Todos</SelectItem>
              <SelectItem value="Premenopáusica">Premenopáusica</SelectItem>
              <SelectItem value="Posmenopáusica">Posmenopáusica</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* BIRADS Filter */}
        <div className="space-y-2">
          <Label htmlFor="birads" className="text-sm font-semibold text-gray-700">
            Clasificación BIRADS
          </Label>
          <Select value={filters.birads} onValueChange={(val) => handleSelectChange('birads', val)}>
            <SelectTrigger id="birads" className="border-pink-200 focus:ring-pink-500">
              <SelectValue placeholder="Seleccione BIRADS" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Todos</SelectItem>
              <SelectItem value="1">BIRADS 1</SelectItem>
              <SelectItem value="2">BIRADS 2</SelectItem>
              <SelectItem value="3">BIRADS 3</SelectItem>
              <SelectItem value="4">BIRADS 4</SelectItem>
              <SelectItem value="5">BIRADS 5</SelectItem>
              <SelectItem value="6">BIRADS 6</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Breastfeeding Filter */}
        <div className="space-y-2">
          <Label htmlFor="breastfeeding" className="text-sm font-semibold text-gray-700">
            Historial de Lactancia
          </Label>
          <Select value={filters.breastfeeding} onValueChange={(val) => handleSelectChange('breastfeeding', val)}>
            <SelectTrigger id="breastfeeding" className="border-pink-200 focus:ring-pink-500">
              <SelectValue placeholder="Seleccione opción" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Todos</SelectItem>
              <SelectItem value="Sí">Sí</SelectItem>
              <SelectItem value="No">No</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Filter Summary */}
        <div className="pt-4 border-t border-pink-100">
          <p className="text-xs text-gray-600 text-center">
            {activeFilters.length === 0 
              ? 'No hay filtros activos - mostrando todos los datos'
              : `${activeFilters.length} filtro${activeFilters.length > 1 ? 's' : ''} activo${activeFilters.length > 1 ? 's' : ''}`
            }
          </p>
        </div>
      </CardContent>
    </Card>
  );
};

export default FilterPanel;

