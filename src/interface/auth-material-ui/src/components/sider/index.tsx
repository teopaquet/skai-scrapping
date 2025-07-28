import React, { useState } from "react";
import {
  type ITreeMenu,
  CanAccess,
  useIsExistAuthentication,
  useTranslate,
  useLogout,
  useMenu,
  useWarnAboutChange,
} from "@refinedev/core";
import { Link } from "react-router";
import { type Sider, ThemedTitleV2 } from "@refinedev/antd";
import { Layout as AntdLayout, Menu, Grid, theme, Button } from "antd";
import {
  LogoutOutlined,
  UnorderedListOutlined,
  RightOutlined,
  LeftOutlined,
} from "@ant-design/icons";
// Styles inline pour moderniser le Sider

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

  const isMobile =
    typeof breakpoint.lg === "undefined" ? false : !breakpoint.lg;

  const renderTreeView = (tree: ITreeMenu[], selectedKey: string) => {
    return tree.map((item: ITreeMenu) => {
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

      if (children.length > 0) {
        const subMenuKey = route || key || name;
        return (
          <Menu.SubMenu
            key={subMenuKey}
            icon={icon ?? <UnorderedListOutlined />}
            title={<span style={{ fontSize: 18, fontWeight: 600 }}>{label}</span>}
          >
            {renderTreeView(children, selectedKey)}
          </Menu.SubMenu>
        );
      }
      const isSelected = route === selectedKey;
      const isRoute = !(parent !== undefined && children.length === 0);
      const itemKey = route || key || name;
      return (
        <CanAccess
          key={itemKey}
          resource={name}
          action="list"
          params={{ resource: item }}
        >
          <Menu.Item
            key={itemKey}
            style={{
              textTransform: "capitalize",
              fontSize: 20,
              fontWeight: 500,
              minHeight: 48,
              display: 'flex',
              alignItems: 'center',
            }}
            icon={icon ?? (isRoute && <UnorderedListOutlined />)}
          >
            {route ? <Link to={route || "/"} style={{ fontSize: 18, fontWeight: 500 }}>{label}</Link> : <span style={{ fontSize: 15, fontWeight: 500 }}>{label}</span>}
            {!collapsed && isSelected && (
              <div className="ant-menu-tree-arrow" />
            )}
          </Menu.Item>
        </CanAccess>
      );
    });
  };

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

  const logout = isExistAuthentication && (
    <Menu.Item key="logout" onClick={handleLogout} icon={<LogoutOutlined />}>
      {translate("buttons.logout", "Logout")}
    </Menu.Item>
  );

  const items = renderTreeView(menuItems, selectedKey);

  const renderSider = () => {
    if (render) {
      return render({
        dashboard: null,
        items,
        logout,
        collapsed,
      });
    }
    return (
      <>
        {items}
        {logout}
      </>
    );
  };

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
      onCollapse={(collapsed: boolean): void => setCollapsed(collapsed)}
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
        <img src="/logo_skai.svg" alt="Skai Visualizer" style={{ height: 32, width: 32, marginRight: collapsed ? 0 : 8 }} />
        {!collapsed && <span style={{ fontFamily: "Roboto, sans-serif" }}>Skai Visualizer</span>}
      </div>
      <div
        style={{
          width: "60%",
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
      >
        {renderSider()}
      </Menu>
    </AntdLayout.Sider>
  );
};
