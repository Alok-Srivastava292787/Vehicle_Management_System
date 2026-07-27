import apiClient from "../api/apiClient";

export const getPartIssues =
  async () => {

    const response =
      await apiClient.get(
        "/part-issues",
        {
          params: {
            _ts: Date.now(),
          },
        }
      );

    return response.data;
  };

export const createPartIssue =
  async (payload) => {

    const response =
      await apiClient.post(
        "/part-issues",
        payload
      );

    return response.data;
  };

export const updatePartIssue =
  async (
    issueId,
    payload
  ) => {

    const response =
      await apiClient.put(
        `/part-issues/${issueId}`,
        payload
      );

    return response.data;
  };

export const deactivatePartIssue =
  async (issueId) => {

    const response =
      await apiClient.delete(
        `/part-issues/${issueId}`
      );

    return response.data;
  };