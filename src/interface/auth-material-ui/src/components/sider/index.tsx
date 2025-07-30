import React, { useState } from "react";
import {
  type ITreeMenu,
  useIsExistAuthentication,
  useTranslate,
  useLogout,
  useMenu,
  useWarnAboutChange,
  useCan,
} from "@refinedev/core";
import { Link } from "react-router";
import { type Sider } from "@refinedev/antd";
import { Layout as AntdLayout, Menu, Grid, theme } from "antd";
import {
  LogoutOutlined,
  UnorderedListOutlined,
} from "@ant-design/icons";

const { useToken } = theme;

export const CustomSider: typeof Sider = ({ render }) => {
  const { token } = useToken();
  const [collapsed, setCollapsed] = useState<boolean>(false);
  const isExistAuthentication = useIsExistAuthentication();
  const { warnWhen, setWarnWhen } = useWarnAboutChange();
  const { mutate: mutateLogout } = useLogout();
  const translate = useTranslate();
  const { menuItems, selectedKey, defaultOpenKeys } = useMenu();
  const breakpoint = Grid.useBreakpoint();
  const isMobile = typeof breakpoint.lg === "undefined" ? false : !breakpoint.lg;
  // Access control is not used for menu items to avoid runtime errors

  const handleLogout = () => {
    if (warnWhen) {
      const confirm = window.confirm(
        translate(
          "warnWhenUnsavedChanges",
          "Are you sure you want to leave? You have unsaved changes.",
        ),
      );
      if (confirm) {
        setWarnWhen(false);
        mutateLogout();
      }
    } else {
      mutateLogout();
    }
  };

  const renderTreeView = (tree: ITreeMenu[], selectedKey: string): any[] => {
    return tree
      .map((item: ITreeMenu) => {
        const { name, children, meta, key, list } = item;
        const icon = meta?.icon
          ? React.isValidElement(meta.icon)
            ? React.cloneElement(meta.icon as React.ReactElement, { style: { fontSize: 22 } })
            : meta.icon
          : <UnorderedListOutlined style={{ fontSize: 28 }} />;
        const label = meta?.label ?? name;
        const parent = meta?.parent;
        const route =
          typeof list === "string"
            ? list
            : typeof list !== "function"
              ? list?.path
              : key;
        const itemKey = route || key || name;
        // Access control removed to avoid runtime error
        if (children.length > 0) {
          return {
            key: itemKey,
            icon: icon ?? <UnorderedListOutlined />,
            label: <span style={{ fontSize: 18, fontWeight: 600 }}>{label}</span>,
            children: renderTreeView(children, selectedKey),
          };
        }
        const isSelected = route === selectedKey;
        const isRoute = !(parent !== undefined && children.length === 0);
        return {
          key: itemKey,
          icon: icon ?? (isRoute && <UnorderedListOutlined />),
          label: route
            ? <Link to={route || "/"} style={{ fontSize: 18, fontWeight: 500 }}>{label}</Link>
            : <span style={{ fontSize: 15, fontWeight: 500 }}>{label}</span>,
          style: {
            textTransform: "capitalize",
            fontSize: 20,
            fontWeight: 500,
            minHeight: 48,
            display: 'flex',
            alignItems: 'center',
          },
          className: !collapsed && isSelected ? "ant-menu-tree-arrow" : undefined,
        };
      })
      .filter(Boolean);
  };

  let items = renderTreeView(menuItems, selectedKey);
  if (isExistAuthentication) {
    items = [
      ...items,
      {
        key: "logout",
        icon: <LogoutOutlined />,
        label: (
          <span onClick={handleLogout} style={{ fontSize: 18, fontWeight: 500 }}>
            {translate("buttons.logout", "Logout")}
          </span>
        ),
        style: {
          textTransform: "capitalize",
          fontSize: 20,
          fontWeight: 500,
          minHeight: 48,
          display: 'flex',
          alignItems: 'center',
        },
      },
    ];
  }

  const siderStyle = {
    margin: '16px',
    borderRadius: '20px',
    boxShadow: '0 8px 24px rgba(25, 118, 210, 0.15)',
    transition: 'box-shadow 0.3s',
    overflow: 'hidden',
    background: 'rgba(255,255,255,0.98)',
    border: 'none',
    position: 'sticky' as React.CSSProperties['position'],
    top: '16px',
    zIndex: 1201,
  };

  return (
    <AntdLayout.Sider
      collapsible
      collapsedWidth={isMobile ? 0 : 80}
      width={280}
      collapsed={collapsed}
      breakpoint="lg"
      onCollapse={(collapsed) => setCollapsed(collapsed)}
      style={{
        ...siderStyle,
        background: !isMobile ? 'transparent' : siderStyle.background,
      }}
      trigger={null}
    >
      <div
        style={{
          width: collapsed ? "80px" : "240px",
          padding: collapsed ? "0" : "0 24px",
          display: "flex",
          justifyContent: collapsed ? "center" : "flex-start",
          alignItems: "center",
          height: "64px",
          background: 'rgba(255,255,255,0.98)',
          fontSize: "16px",
          fontWeight: "bold",
          color: "#1976d2",
          cursor: 'pointer',
        }}
        onClick={() => setCollapsed(!collapsed)}
      >
        <img src="/logo_skai.svg" alt="SkAI Visualizer" style={{ height: 32, width: 62, marginRight: collapsed ? 0 : 8 }} />
        {!collapsed && (
          <span
            style={{
              fontFamily: 'Montserrat, Roboto, sans-serif',
              fontWeight: 600,
              fontSize: 20,
              letterSpacing: 1.2,
              color: '#1976d2',
              textShadow: '0 6px 8px rgba(25,118,210,0.08)',
              lineHeight: 1.1,
              marginLeft: 4,
            }}
          >
            SkAI Visualizer
          </span>
        )}
      </div>
      <div
        style={{
          width: "70%",
          height: 0,
          borderBottom: "2.5px solid #1976d2",
          margin: "0 auto"
        }}
      />
      <Menu
        defaultOpenKeys={defaultOpenKeys}
        selectedKeys={[selectedKey]}
        mode="inline"
        style={{
          marginTop: "8px",
          border: "none",
          background: 'rgba(255,255,255,0.98)',
        }}
        onClick={() => {
          if (!breakpoint.lg) {
            setCollapsed(true);
          }
        }}
        items={items}
      />
    </AntdLayout.Sider>
  );
};
