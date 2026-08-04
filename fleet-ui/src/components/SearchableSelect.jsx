import { Select } from "antd";

export const SearchableSelect =
  (props) => (
    <Select
      showSearch
      optionFilterProp="label"
      allowClear
      {...props}
    />
  );