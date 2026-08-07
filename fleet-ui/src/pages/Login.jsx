import {
  Button,
  Card,
  Form,
  Input,
  message,
} from "antd";

import {
  useNavigate,
} from "react-router-dom";

import apiClient from "../api/apiClient";

export default function Login() {

  const navigate =
    useNavigate();

  const onFinish =
    async values => {

      try {

        const params =
          new URLSearchParams();

        params.append(
          "username",
          values.username
        );

        params.append(
          "password",
          values.password
        );

        const response =
          await apiClient.post(
            "/auth/login",
            params,
            {
              headers: {
                "Content-Type":
                  "application/x-www-form-urlencoded",
              },
            }
          );

        localStorage.setItem(
          "token",
          response.data.access_token
        );

        localStorage.setItem(
          "username",
          response.data.username
        );

        localStorage.setItem(
          "employee_id",
          response.data.employee_id
        );

        message.success(
          "Login successful"
        );

        navigate("/");
      }
      catch {

        message.error(
          "Invalid credentials"
        );
      }
    };

  return (

    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
      }}
    >

      <Card
        title="Fleet Management Login"
        style={{
          width: 400,
        }}
      >

        <Form
          onFinish={onFinish}
          layout="vertical"
        >

          <Form.Item
            label="Username"
            name="username"
            rules={[
              {
                required: true,
              },
            ]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="Password"
            name="password"
            rules={[
              {
                required: true,
              },
            ]}
          >
            <Input.Password />
          </Form.Item>

          <Button
            type="primary"
            htmlType="submit"
            block
          >
            Login
          </Button>

        </Form>

      </Card>

    </div>
  );
}
