import pandas as pd
import matplotlib.pyplot as plt


def st_heat_amount(components_df, pv_st, dataframe, amounts_dict):
    from program_files.postprocessing.plotting import get_pv_st_dir, get_value

    df_pv_or_st = components_df[(components_df.isin([str(pv_st)])).any(axis=1)]
    for num, comp in df_pv_or_st.iterrows():
        value_am = get_value(comp["label"], "output 1/kWh", dataframe)
        amounts_dict["ST"].append(value_am)
        # TODO wie stellen wir fest ob -180 - 180 oder 0 - 360
        #  genutzt wurde
        amounts_dict = get_pv_st_dir(amounts_dict, value_am, "ST", comp)
    return amounts_dict


def create_heat_amount_plots(dataframes: dict, nodes_data, result_path, sink_known):
    """ """
    from program_files.postprocessing.plotting import (
        get_dataframe_from_nodes_data,
        get_value,
    )

    heat_amounts = pd.DataFrame()
    heat_amounts_dict = {}
    emissions_100_percent = sum(dataframes["1"]["constraints/CU"])
    for key in dataframes:
        heat_amounts_dict.update(
            {
                "run": str(key),
                "ST": [],
                "Electric_heating": [],
                "Gasheating": [],
                "HeatPump": [],
                "DH": [],
                "Heat_Demand": [],
                "Thermalstorage_losses": [],
                "Thermalstorage_output": [],
                "ST_north": [],
                "ST_north_east": [],
                "ST_east": [],
                "ST_south_east": [],
                "ST_south": [],
                "ST_south_west": [],
                "ST_west": [],
                "ST_north_west": [],
                "GCHP": [],
                "ASHP": [],
                "Insulation": [],
                "central_heat_production": [],
                "reductionco2": (
                    sum(dataframes[key]["constraints/CU"]) / emissions_100_percent
                )
                if key != "0"
                else (
                    (
                        sum(dataframes[key]["periodical costs/CU"])
                        + sum(dataframes[key]["variable costs/CU"])
                    )
                    / emissions_100_percent
                ),
            }
        )
        dataframe = dataframes[key].copy()
        dataframe.reset_index(inplace=True, drop=False)
        components_df = get_dataframe_from_nodes_data(nodes_data)
        # TODO concentrated solar power
        heat_amounts_dict = st_heat_amount(
            components_df, "solar_thermal_flat_plate", dataframe, heat_amounts_dict
        )
        # heat pump dataframe
        df_hp = components_df[
            (components_df.isin(["CompressionHeatTransformer"])).any(axis=1)
        ]
        df_hp = pd.concat(
            [df_hp, (components_df.isin(["AbsorptionHeatTransformer"])).any(axis=1)]
        )
        # collect electric input flow of Heat Pumps
        for num, comp in df_hp.iterrows():
            if comp["heat source"] == "Ground":
                heat_amounts_dict["GCHP"].append(
                    get_value(comp["label"], "output 1/kWh", dataframe)
                )
            elif comp["heat source"] == "Air":
                # ashp heat output
                heat_amounts_dict["ASHP"].append(
                    get_value(comp["label"], "output 1/kWh", dataframe)
                )
        # sink dataframe
        df_sinks = components_df[(components_df["annual demand"].notna())]
        df_sinks = pd.concat(
            [df_sinks, components_df[(components_df["nominal value"].notna())]]
        ).drop_duplicates()
        # collect the amount of electricity demand
        for num, sink in df_sinks.iterrows():
            if sink_known[sink["label"]][1]:
                heat_amounts_dict["Heat_Demand"].append(
                    get_value(sink["label"], "input 1/kWh", dataframe)
                )

        df_storage = components_df[(components_df.isin(["Generic"])).any(axis=1)]
        for num, storage in df_storage.iterrows():
            # collect thermalstorage output and losses of an active
            # storage
            if "heat" in storage["bus"] and "central" not in storage["bus"]:
                value = get_value(storage["label"], "output 1/kWh", dataframe)
                heat_amounts_dict["Thermalstorage_output"].append(value)
                input_val = get_value(storage["label"], "input 1/kWh", dataframe)
                heat_amounts_dict["Thermalstorage_losses"].append(input_val - value)
        # generic transformer dataframe
        df_gen_transformer = components_df[
            (components_df.isin(["GenericTransformer"])).any(axis=1)
        ]
        for num, transformer in df_gen_transformer.iterrows():
            # collecting GenericTransformer with electric input
            # (Electric Heating)
            if (
                ("heat" in transformer["output"] or "heat" in transformer["output2"])
                and "central" not in transformer["input"]
                and "elec" in transformer["input"]
            ):
                heat_amounts_dict["Electric_heating"].append(
                    get_value(transformer["label"], "output 1/kWh", dataframe)
                )
            elif (
                ("heat" in transformer["output"] or "heat" in transformer["output2"])
                and "central" not in transformer["input"]
                and "gas" in transformer["input"]
            ):
                heat_amounts_dict["Gasheating"].append(
                    get_value(transformer["label"], "output 1/kWh", dataframe)
                )
        df_insulation = components_df[components_df["U-value new"].notna()]
        # collects insulation output flows
        for num, insulation in df_insulation.iterrows():
            cap_sink = get_value(insulation["sink"], "capacity/kW", dataframe)
            cap_insulation = get_value(insulation["label"], "capacity/kW", dataframe)
            value_sink = get_value(insulation["sink"], "input 1/kWh", dataframe)
            if cap_insulation != 0 and cap_sink != 0:
                heat_amounts_dict["Insulation"].append(
                    ((cap_insulation * value_sink) / cap_sink)
                )

        heat_amounts_dict["DH"] += list(
            dataframe.loc[dataframe["ID"].str.startswith("dh_heat_house_station")][
                "output 1/kWh"
            ].values
        )

        for i in heat_amounts_dict:
            if i != "run" and i != "reductionco2":
                heat_amounts_dict[i] = sum(heat_amounts_dict[i])
        series = pd.Series(data=heat_amounts_dict)
        heat_amounts = pd.concat([heat_amounts, pd.DataFrame([series])])
        heat_amounts.set_index("reductionco2", inplace=True, drop=False)
        heat_amounts = heat_amounts.sort_values("run")
    # HEAT PLOT
    fig, axs = plt.subplots(3, sharex="all")
    fig.set_size_inches(18.5, 15.5)
    plot_dict = {
        axs[0]: {
            "SLP_DEMAND": heat_amounts.Heat_Demand,
            "Thermalstorage losses": heat_amounts.Thermalstorage_losses,
            "Insulation": heat_amounts.Insulation,
        },
        axs[1]: {
            "Electric Heating": heat_amounts.Electric_heating,
            "Gasheating": heat_amounts.Gasheating,
            "ASHP": heat_amounts.ASHP,
            "GCHP": heat_amounts.GCHP,
            "DH": heat_amounts.DH,
            "ST": heat_amounts.ST,
        },
        axs[2]: {
            "ST_north": heat_amounts.ST_north,
            "ST_north_east": heat_amounts.ST_north_east,
            "ST_east": heat_amounts.ST_east,
            "ST_south_east": heat_amounts.ST_south_east,
            "ST_south": heat_amounts.ST_south,
            "ST_south_west": heat_amounts.ST_south_west,
            "ST_west": heat_amounts.ST_west,
            "ST_north_west": heat_amounts.ST_north_west,
        },
    }
    for plot in plot_dict:
        plot.stackplot(
            heat_amounts.reductionco2,
            plot_dict.get(plot).values(),
            labels=list(plot_dict.get(plot).keys()),
        )
    axs[0].invert_xaxis()
    axs[0].legend()
    axs[0].set_ylabel("Heat Amount in kWh")
    axs[1].legend()
    axs[1].set_ylabel("Heat Amount in kWh")
    axs[2].legend(loc="upper left")
    axs[2].set_ylabel("Heat Amount in kWh")
    axs[2].set_xlabel("Emission-reduced Scenario")
    plt.savefig(result_path + "/heat_amounts.jpeg")
