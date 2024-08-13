import axios from 'axios';
import API_BASE_URL from './config';

// Example function to fetch all items of a specific model
export const fetchAllItems = async (model) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/${model}/`);
        return response.data;
    } catch (error) {
        console.error("Error fetching items:", error);
        throw error;
    }
};

// Example function to fetch a single item by ID
export const fetchItemById = async (model, id) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/${model}/${id}/`);
        return response.data;
    } catch (error) {
        console.error("Error fetching item:", error);
        throw error;
    }
};

// Example function to create a new item
export const createItem = async (model, data) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/${model}/`, data);
        return response.data;
    } catch (error) {
        console.error("Error creating item:", error);
        throw error;
    }
};

// Example function to update an item
export const updateItem = async (model, id, data) => {
    try {
        const response = await axios.put(`${API_BASE_URL}/${model}/${id}/`, data);
        return response.data;
    } catch (error) {
        console.error("Error updating item:", error);
        throw error;
    }
};

// Example function to delete an item
export const deleteItem = async (model, id) => {
    try {
        await axios.delete(`${API_BASE_URL}/${model}/${id}/`);
    } catch (error) {
        console.error("Error deleting item:", error);
        throw error;
    }
};
