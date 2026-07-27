import apiClient from "../api/apiClient";

export const getPartIssueDetails =
  async () => {

    const response =
      await apiClient.get(
        "/part-issue-details",
        {
          params: {
            _ts: Date.now(),
          },
        }
      );

    return response.data;
  };

export const createPartIssueDetail =
  async (payload) => {

    const response =
      await apiClient.post(
        "/part-issue-details",
        payload
      );

    return response.data;
  };

export const updatePartIssueDetail =
  async (
    issueDetailId,
    payload
  ) => {

    const response =
      await apiClient.put(
        `/part-issue-details/${issueDetailId}`,
        payload
      );

    return response.data;
  };

export const deactivatePartIssueDetail =
  async (
    issueDetailId
  ) => {

    const response =
      await apiClient.delete(
        `/part-issue-details/${issueDetailId}`
      );

    return response.data;
  };