import { DataProvider } from "@refinedev/core";
import { apiService } from "./apiService";

export const dataProvider = (): DataProvider => ({
  getList: async ({ resource, pagination, filters, sorters, meta }) => {
    const params: any = {};

    // Handle pagination
    if (pagination?.current && pagination?.pageSize) {
      params._start = (pagination.current - 1) * pagination.pageSize;
      params._end = pagination.current * pagination.pageSize;
    }

    // Handle sorting
    if (sorters && sorters.length > 0) {
      params._sort = sorters[0].field;
      params._order = sorters[0].order;
    }

    // Handle filters
    if (filters) {
      filters.forEach((filter) => {
        if (filter.operator === "eq") {
          params[filter.field] = filter.value;
        }
        // Add more filter operators as needed
      });
    }

    try {
      const data = await apiService.get(`/${resource}`, params);
      
      return {
        data: Array.isArray(data) ? data : data.data || [],
        total: data.total || data.length || 0,
      };
    } catch (error) {
      throw error;
    }
  },

  getOne: async ({ resource, id, meta }) => {
    try {
      const data = await apiService.get(`/${resource}/${id}`);
      return {
        data,
      };
    } catch (error) {
      throw error;
    }
  },

  create: async ({ resource, variables, meta }) => {
    try {
      const data = await apiService.post(`/${resource}`, variables);
      return {
        data,
      };
    } catch (error) {
      throw error;
    }
  },

  update: async ({ resource, id, variables, meta }) => {
    try {
      const data = await apiService.put(`/${resource}/${id}`, variables);
      return {
        data,
      };
    } catch (error) {
      throw error;
    }
  },

  deleteOne: async ({ resource, id, meta }) => {
    try {
      await apiService.delete(`/${resource}/${id}`);
      return {
        data: { id } as any,
      };
    } catch (error) {
      throw error;
    }
  },

  getApiUrl: () => apiService.getInstance().defaults.baseURL || "",

  // Custom method for bulk operations
  deleteMany: async ({ resource, ids, meta }) => {
    try {
      const promises = ids.map((id) => apiService.delete(`/${resource}/${id}`));
      await Promise.all(promises);
      return {
        data: ids.map((id) => ({ id })) as any,
      };
    } catch (error) {
      throw error;
    }
  },

  updateMany: async ({ resource, ids, variables, meta }) => {
    try {
      const promises = ids.map((id) => 
        apiService.put(`/${resource}/${id}`, variables)
      );
      const results = await Promise.all(promises);
      return {
        data: results,
      };
    } catch (error) {
      throw error;
    }
  },

  createMany: async ({ resource, variables, meta }) => {
    try {
      const promises = variables.map((data: any) => 
        apiService.post(`/${resource}`, data)
      );
      const results = await Promise.all(promises);
      return {
        data: results,
      };
    } catch (error) {
      throw error;
    }
  },
});

export default dataProvider;
