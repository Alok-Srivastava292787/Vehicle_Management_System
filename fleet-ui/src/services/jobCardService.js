import apiClient from "../api/apiClient";

export const getJobCards = async () => {
    const response = await apiClient.get("/jobcards",{params: { _ts: Date.now(),},}
      );

    return response.data;
  };

export const createJobCard = async (payload) => {
    const response = await apiClient.post("/jobcards",payload
      );

    return response.data;
  };

export const updateJobCard = async (jobCardId,payload) => {
    const response = await apiClient.put(`/jobcards/${jobCardId}`,payload
      );

    return response.data;
  };

export const deactivateJobCard =async (jobCardId) => {
    const response = await apiClient.put(`/jobcards/${jobCardId}`,{active_flag: false,}
      );

    return response.data;
  };

export const generateRequisition = async jobCardId => {
    const response =await apiClient.post(`/jobcards/${jobCardId}/generate-requisition`
      );

    return response.data;
  };

export const submitJobCard =
  async jobCardId => {

    const response =
      await apiClient.post(
        `/jobcards/${jobCardId}/submit`
      );

    return response.data;
  };

export const verifyJobCard =
  async jobCardId => {

    const response =
      await apiClient.post(
        `/jobcards/${jobCardId}/verify`
      );

    return response.data;
  };

export const approveJobCard =
  async jobCardId => {

    const response =
      await apiClient.post(
        `/jobcards/${jobCardId}/approve`
      );

    return response.data;
  };